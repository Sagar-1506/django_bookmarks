from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

from bookmarks.models import *
class RegistrationForm(forms.Form):
    
    username=forms.CharField(label='username',max_length=30)
    email=forms.EmailField(label='email')
    password1=forms.CharField(label='password',widget=forms.PasswordInput())
    password2=forms.CharField(label='Confirm password',widget=forms.PasswordInput())

    def clean_password2(self):
        
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data :
            
            
            password1=self.cleaned_data['password1']
        
            password2=self.cleaned_data['password2']
            
            if len(password1)<8 :
                raise forms.ValidationError("Password must contain 8 characters")
       
            
            if password1 != password2 :
                raise forms.ValidationError('Passwords do not match')
            return password2
        
        raise forms.ValidationError('error in passwords')
        
        
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError('Username can contain only alphanumeric characters and underscore')
        try :
            user=User.objects.get(username=username)
        except ObjectDoesNotExist :
            return username
        
        raise forms.ValidationError('Username already taken.')
    
    def clean_email(self):
        email=self.cleaned_data['email']
        
        try :
            user=User.objects.get(email=email)
        except ObjectDoesNotExist :
            return email
        
        raise forms.ValidationError('Email already registered.')


class BookmarkSaveForm(forms.Form):
    url=forms.URLField(label="URL" ,widget=forms.TextInput(attrs={'size':64}))
    title=forms.CharField(label="Title",widget=forms.TextInput(attrs={'size':64}))
    tags=forms.CharField(label="Tags",required=False,widget=forms.TextInput(attrs={'size':64}))
    share = forms.BooleanField(label="share on main page ",required=False)
    
    
    
class SearchForm(forms.Form):
    query=forms.CharField(label="Enter keyword to search",widget=forms.TextInput(attrs={'size':64}))
    

class MessageForm(forms.Form):
    to_user=forms.CharField(max_length=100)
    from_user=forms.CharField(max_length=100)
    content=forms.CharField(widget=forms.Textarea())
    
    
    def clean_to_user(self):
        try :
            
            user=User.objects.get(username=self.cleaned_data['to_user'])
        except ObjectDoesNotExist :
            raise forms.ValidationError("User not found")
        
        return user
        
    
    