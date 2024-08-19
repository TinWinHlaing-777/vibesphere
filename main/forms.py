from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import BlogPage, Article

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
            'title': forms.TextInput(attrs={'class': 'page__form__input'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'page__form__input'}),
            'meta_description': forms.Textarea(attrs={'class': 'page__form__input', 'placeholder': 'Describe the aim and purpose of creating this page in a few words.'}),
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'page__form__input'}),
            'status': forms.Select(choices=[('draft', 'Draft'), ('published', 'Published')], attrs={'class': 'page__form__input'}),
        }

class ArticleForm(forms.ModelForm):
    page_name = forms.CharField(label='Page Name', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Article
        fields = [
            'title',
            'page_name',
            'article_image',
            'content',
            'published_date',
            'allow_to_comment',
            'view_count',
            'category',
            'tag'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'article_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'allow_to_comment': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_page_name(self):
        page_name = self.cleaned_data.get('page_name')
        try:
            blog_page = BlogPage.objects.get(title=page_name)
        except BlogPage.DoesNotExist:
            raise forms.ValidationError(f"BlogPage with title '{page_name}' does not exist.")
        return blog_page 

    
