from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import Profile

#################### Custom Login Form for changing field labels ####################

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label = 'Username or Email',
        widget = forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control mb-3'
            })
    )

#################### Form for Registration ####################

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']