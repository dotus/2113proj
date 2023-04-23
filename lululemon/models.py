# Create your models here.
#lululemon.models.py
from io import BytesIO
import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw

class LogMessage(models.Model):
    staffname = models.CharField(max_length=200,help_text="Enter username:") #who is using it
    product=models.TextField(default ='product',max_length=300,help_text="Enter Product:")
    log_date = models.DateTimeField("date logged",default=timezone.datetime.now) #check_out date
    available = models.BooleanField(default=True)

    def __str__(self):
        """Returns a string representation of a message."""
        #date = timezone.localtime(self.log_date)
        return f"{self.product}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class Category(models.Model):
    categoryName = models.CharField(max_length=300, help_text="Type in the Category of the Item")
    def __str__(self):
        return self.categoryName
    
class Item(models.Model):
    staffname = models.CharField(max_length=200,default='lululemon employee') #who is using it
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.CharField(default='product', max_length=200)
    qr_code = models.ImageField(blank=True, null=True, upload_to="QR_CODE/")
    color = models.CharField(max_length=13, default='Black')
    size = models.CharField(max_length=13, default='S/M/L')
    available_quantity = models.PositiveIntegerField(default=0)
    checkin_quantity=models.PositiveIntegerField(default=0)
    checkout_quantity=models.PositiveIntegerField(default=0)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product
    
    def save(self, *args, **kwargs):
        # Generate UUID for the item
        if not self.id:
            self.id = uuid.uuid4()

        # Generate QR code and save to file
        qr = f"{self.product}, {self.id}"
        qr_code = qrcode.make(qr)
        qr_offset = Image.new('RGB', qr_code.size, 'white')
        draw_img = ImageDraw.Draw(qr_offset)
        qr_offset.paste(qr_code)

        file_name = f"{self.product}-{self.id}.png"
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False)
        qr_offset.close()

        # Call the superclass save method to save the item to the database
        super().save(*args, **kwargs)       

    def get_absolute_url(self):
        return reverse("item_detail", args=[str(self.pk)])

class Action(models.Model):
    ACTION_CHOICES = (
        ('checkin', 'Check-in'),
        ('checkout', 'Check-out'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.quantity} - {self.created_at}"
    def display_action(self):
        for choice in Action._meta.get_field('action_type').choices:
            if choice[0] == self.action_type:
                return choice[1]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
