from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ask_yakovitskiy.models import Question, Answer, Profile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class NewQuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    
    class Meta:
        model = Question
        fields = ['title', 'text']
        
class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['text']
        
class UserForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email']

class SettingsForm(forms.Form):
    username = forms.CharField(required=True, label='nick-name')
    email = forms.EmailField(required=True,
                             label='email adress',
                             help_text='your email adress wont be shown to anybody else')
    new_password = forms.CharField(required=False, widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(required=False, widget=forms.PasswordInput())
    avatar = forms.ImageField(required=False)
    old_password = forms.CharField(required=True,
                                   widget=forms.PasswordInput(),
                                   help_text='Enter your current password, to apply changes')
    
class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['avatar']
        