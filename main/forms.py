from django import forms
from django.contrib.auth.hashers import make_password
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'reg__input', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'reg__input', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'nick_name', 'email', 'phone_number', 
            'nationality', 'country', 'city', 'postal_code', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'Last Name'}),
            'nick_name': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'Nick Name'}),
            'email': forms.EmailInput(attrs={'class': 'reg__input', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'Phone Number'}),
            'nationality': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'Nationality'}),
            'country': forms.TextInput(attrs={'class': 'reg__input', 'placeholder':'Country'}),
            'city': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'reg__input', 'placeholder': 'Postal Code'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'reg__input', 'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'reg__input', 'placeholder': 'Password'}))

# class ProfileImageForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['profile_image']
    
