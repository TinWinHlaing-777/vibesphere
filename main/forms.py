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
    def __init__(self, *args, **kwargs):
        is_editing = kwargs.pop('is_editing', False)
        super(BlogPageForm, self).__init__(*args, **kwargs)

        # If the form is in edit mode, make the title field read-only
        if is_editing:
            self.fields['title'].widget.attrs['readonly'] = True
            self.fields['title'].widget.attrs['class'] += ' form__input--readonly'

    class Meta:
        model = BlogPage
        fields = [
            'title',
            'profile_image',
            'meta_description',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form__input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form__input', 'placeholder': 'Describe the aim and purpose of creating this page in a few words.'}),
            'status': forms.Select(choices=[('draft', 'Draft'), ('published', 'Published')], attrs={'class': 'form__input'}),
        }

class ArticleForm(forms.ModelForm):
    page_name = forms.ModelChoiceField(
        queryset=BlogPage.objects.none(), 
        widget=forms.Select(attrs={'class': 'form__input'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        is_editing = kwargs.pop('is_editing', False)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['page_name'].queryset = BlogPage.objects.filter(author=user)

        # If the form is in edit mode, make the title field read-only
        if is_editing:
            self.fields['title'].widget.attrs['readonly'] = True
            self.fields['title'].widget.attrs['class'] += ' form__input--readonly'

    def clean_page_name(self):
        page_name = self.cleaned_data.get('page_name')
        if not page_name:
            raise forms.ValidationError("Page name is required.")
        return page_name

    class Meta:
        model = Article
        fields = [
            'title',
            'page_name',
            'article_image',
            'content',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input'}),
            'article_image': forms.ClearableFileInput(attrs={'class': 'form__input'}),
            'content': forms.Textarea(attrs={'class': 'form__input'}),
            'category': forms.Select(attrs={'class': 'form__input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your vibe here...', 'rows': 1, 'class': 'comment__form__input'}),
        }
