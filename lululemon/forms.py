# lululemon.forms.py
from django import forms
from lululemon.models import LogMessage, Category
#from lululemon.models import Accessories, LogMessage, Men, Women
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Action, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from lululemon.models import Item, UserProfile

    
class ItemForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    quantity = forms.IntegerField(required=False)
    operation = forms.ChoiceField(choices=(('check_in', 'Check In'), ('check_out', 'Check Out')), required=False)
    checkin_quantity = forms.IntegerField(required=False)
    checkout_quantity = forms.IntegerField(required=False)

    class Meta:
        model = Item
        fields = ['staffname', 'product', 'color', 'size', 'categories', 'quantity', 'operation', 'checkin_quantity', 'checkout_quantity']

class NewItemForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Item
        fields = ['staffname', 'product', 'color', 'size', 'available_quantity', 'categories']

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']
class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("staffname","product",)

class CheckInOutForm(forms.Form):
    check_in = forms.BooleanField(required=False)
    check_out = forms.BooleanField(required=False)
    check_in_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())
    check_out_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())

class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control',}))
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password','id': 'password',}))
    password2 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control','data-toggle': 'password','id': 'password',}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control',}))
    password = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','data-toggle': 'password','id': 'password','name': 'password',}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']