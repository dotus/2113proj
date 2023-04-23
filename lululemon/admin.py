from django.contrib import admin

# Register your models here.
from django.contrib import admin 
from lululemon.models import LogMessage, Item, Category, Action
#from lululemon.models import Women 
#from lululemon.models import Men
#from lululemon.models import Accessories
from django.contrib.auth.admin import UserAdmin
from .models import Profile

admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Category)
class HelloAdmin(admin.ModelAdmin):
  search_fields = ['staffname',]
admin.site.register(LogMessage,HelloAdmin)
admin.site.register(Action)
