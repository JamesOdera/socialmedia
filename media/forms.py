from django.contrib.auth.models import User
from .models import *
from django import forms


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'image',)
        
        labels = {
           'body' : '',
           'image' : '',
        }
        
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder':'Share Something...'
            }),
        }
        
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'image',)
        
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
            }),
            'image': forms.FileInput(attrs={
                
            }),
        }
        
class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Enter username...'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password...'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password...'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password...'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        help_texts = {
            'username': None,
            'email': None,
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password Missmatch')
        return confirm_password
    
class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'followers',)
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder':'Share Something about yourself...'
            }),
            'photo': forms.FileInput(attrs={
                
            }),
        }
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control',
               'style': 'width: 100%',
               'placeholder': 'Write a comment', 'rows': '3', }))

    class Meta:
        model = Comment
        fields = ('content',)
        
class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)
        
class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=100)
    image = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(
            attrs={"class": "imagefile",}
        ))
    class Meta:
        model = MessageModel
        fields = ['body','image']

        