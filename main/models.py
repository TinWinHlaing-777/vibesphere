from django.db import models
from django.utils.translation import gettext_lazy as _

# User Model
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nick_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to="profile/")
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    def __str__(self):
        return self.email
    
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_date = models.DateTimeField(auto_now_add=True)
    viewer_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def author_name(self):
        return f"{self.author.first_name} {self.author.last_name}"

    @property
    def author_email(self):
        return self.author.email