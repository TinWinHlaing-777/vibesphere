from django.db import models
from django.contrib.auth.models import User
from django.db import models

CATEGORY_CHOICES = [
        ('Local News', 'Local News'),
        ('International News', 'International News'),
        ('Politics', 'Politics'),
        ('Crime', 'Crime'),
        ('Business', 'Business'),
        ('Finance', 'Finance'),
        ('Economy', 'Economy'),
        ('Entrepreneurship', 'Entrepreneurship'),
        ('Real Estate', 'Real Estate'),
        ('Technology', 'Technology'),
        ('Gadgets', 'Gadgets'),
        ('Software', 'Software'),
        ('Startups', 'Startups'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Lifestyle', 'Lifestyle'),
        ('Travel', 'Travel'),
        ('Fashion', 'Fashion'),
        ('Food & Drink', 'Food & Drink'),
        ('Health & Fitness', 'Health & Fitness'),
        ('Relationships', 'Relationships'),
        ('Entertainment', 'Entertainment'),
        ('Movies', 'Movies'),
        ('Music', 'Music'),
        ('Television', 'Television'),
        ('Celebrity News', 'Celebrity News'),
        ('Sports', 'Sports'),
        ('Football/Soccer', 'Football/Soccer'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Motorsports', 'Motorsports'),
        ('Science', 'Science'),
        ('Space', 'Space'),
        ('Biology', 'Biology'),
        ('Physics', 'Physics'),
        ('Environmental Science', 'Environmental Science'),
        ('Culture', 'Culture'),
        ('Art', 'Art'),
        ('History', 'History'),
        ('Literature', 'Literature'),
        ('Philosophy', 'Philosophy'),
        ('Education', 'Education'),
        ('Higher Education', 'Higher Education'),
        ('Online Learning', 'Online Learning'),
        ('Career Advice', 'Career Advice'),
        ('Academic Research', 'Academic Research'),
        ('Opinion', 'Opinion'),
        ('Editorials', 'Editorials'),
        ('Op-Eds', 'Op-Eds'),
        ('Letters to the Editor', 'Letters to the Editor'),
        ('Automotive', 'Automotive'),
        ('Car Reviews', 'Car Reviews'),
        ('Auto Industry News', 'Auto Industry News'),
        ('Maintenance Tips', 'Maintenance Tips'),
        ('Motorcycles', 'Motorcycles'),
        ('Home & Garden', 'Home & Garden'),
        ('Interior Design', 'Interior Design'),
        ('Gardening', 'Gardening'),
        ('DIY Projects', 'DIY Projects'),
        ('Home Improvement', 'Home Improvement'),
        ('Personal Finance', 'Personal Finance'),
        ('Investing', 'Investing'),
        ('Banking', 'Banking'),
        ('Insurance', 'Insurance'),
        ('Mental Health', 'Mental Health'),
        ('Medical News', 'Medical News'),
        ('Nutrition', 'Nutrition'),
        ('Fitness', 'Fitness'),
        ('Domestic Politics', 'Domestic Politics'),
        ('International Relations', 'International Relations'),
        ('Political Analysis', 'Political Analysis'),
        ('Policy', 'Policy'),
        ('Innovations', 'Innovations'),
        ('Scientific Discoveries', 'Scientific Discoveries'),
        ('Tech Reviews', 'Tech Reviews'),
        ('Space Exploration', 'Space Exploration'),
        ('Climate Change', 'Climate Change'),
        ('Conservation', 'Conservation'),
        ('Sustainability', 'Sustainability'),
        ('Wildlife', 'Wildlife'),
        ('Religious News', 'Religious News'),
        ('Spiritual Guidance', 'Spiritual Guidance'),
        ('Faith Discussions', 'Faith Discussions'),
        ('Theology', 'Theology'),
        ('Video Games', 'Video Games'),
        ('Board Games', 'Board Games'),
        ('Game Reviews', 'Game Reviews'),
        ('eSports', 'eSports'),
        ('Pregnancy', 'Pregnancy'),
        ('Child Development', 'Child Development'),
        ('Parenting Tips', 'Parenting Tips'),
        ('Family Activities', 'Family Activities'),
    ]
class BlogPage(models.Model):
    title = models.CharField(primary_key=True, unique=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='blog_images/')
    meta_description = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('draft', 'Pending'), ('published', 'Published')], default='draft')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Article(models.Model):
    title = models.CharField(primary_key=True, unique=True, max_length=200)
    page_name = models.ForeignKey(BlogPage, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    article_image = models.ImageField(upload_to='article_images/')
    content = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    allow_to_comment = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'



    