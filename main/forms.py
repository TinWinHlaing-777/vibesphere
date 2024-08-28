from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import BlogPage, Article, Comment
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget= forms.EmailInput(attrs={
            'class': 'reg__input',
            'placeholder': 'Email address'
        }),
        label=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'reg__input',
            'placeholder': 'Enter your new password',
        }),
        label=False
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'reg__input',
            'placeholder': 'Confirm your password',
        }),
        label=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'reg__input',
                'placeholder': 'Enter your username',
            }),
        }
        labels = {
            'username': False,
        }
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not username.isalnum():
            raise ValidationError('Username cannot contain any space.')
        return username

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget = forms.TextInput(attrs={
            'class': 'reg__input',
            'placeholder': 'Enter your username'
        }),
        label=False
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'reg__input',
            'placeholder': 'Enter your new password'
        }),
        label=False
    )

class BlogPageForm(forms.ModelForm):
    class Meta:
        model = BlogPage
        fields = [
            'title',
            'profile_image',
            'meta_description',
            'published_date',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form__input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form__input', 'placeholder': 'Describe the aim and purpose of creating this page in a few words.'}),
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form__input'}),
            'status': forms.Select(choices=[('draft', 'Draft'), ('published', 'Published')], attrs={'class': 'form__input'}),
        }

class ArticleForm(forms.ModelForm):
    page_name = forms.CharField(label='Page Name', max_length=200, widget=forms.TextInput(attrs={'class': 'form__input'}))

    class Meta:
        model = Article
        fields = [
            'title',
            'page_name',
            'article_image',
            'content',
            'published_date',
            'allow_to_comment',
            'category',
            'tag'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input'}),
            'article_image': forms.ClearableFileInput(attrs={'class': 'form__input'}),
            'content': forms.Textarea(attrs={'class': 'form__input'}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form__input', 'type': 'datetime-local'}),
            'allow_to_comment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form__input'}),
            'tag': forms.Select(attrs={'class': 'form__input'}),
        }

    def clean_page_name(self):
        page_name = self.cleaned_data.get('page_name')
        try:
            blog_page = BlogPage.objects.get(title=page_name)
        except BlogPage.DoesNotExist:
            raise forms.ValidationError(f"BlogPage with title '{page_name}' does not exist.")
        return blog_page 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your comment here...', 'rows': 4}),
        }
