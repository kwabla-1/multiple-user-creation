from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .forms import UserChangeForm, UserCreationForm
user = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_filter = ["is_superuser"]
    list_display =  ["username","first_name","last_name", "email", 'user_type']
    
    fieldsets = [
        (None, {"fields": [ "password","first_name", "last_name"]}),
        ("Personal info", {"fields": ["email", "username","user_type"]}),
    ]
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )   
    
    search_fields = ['username',"email"]
    ordering = ["username"]
    
    
admin.site.register(user, UserAdmin)