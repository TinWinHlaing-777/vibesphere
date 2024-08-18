# Generated by Django 4.2.15 on 2024-08-15 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0014_rename_featured_image_blogpage_profile_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('title', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('article_image', models.ImageField(blank=True, null=True, upload_to='article_images/')),
                ('content', models.TextField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('allow_to_comment', models.BooleanField(default=True)),
                ('view_count', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('Local News', 'Local News'), ('International News', 'International News'), ('Politics', 'Politics'), ('Crime', 'Crime'), ('Business', 'Business'), ('Finance', 'Finance'), ('Economy', 'Economy'), ('Entrepreneurship', 'Entrepreneurship'), ('Real Estate', 'Real Estate'), ('Technology', 'Technology'), ('Gadgets', 'Gadgets'), ('Software', 'Software'), ('Startups', 'Startups'), ('Artificial Intelligence', 'Artificial Intelligence'), ('Lifestyle', 'Lifestyle'), ('Travel', 'Travel'), ('Fashion', 'Fashion'), ('Food & Drink', 'Food & Drink'), ('Health & Fitness', 'Health & Fitness'), ('Relationships', 'Relationships'), ('Entertainment', 'Entertainment'), ('Movies', 'Movies'), ('Music', 'Music'), ('Television', 'Television'), ('Celebrity News', 'Celebrity News'), ('Sports', 'Sports'), ('Football/Soccer', 'Football/Soccer'), ('Basketball', 'Basketball'), ('Tennis', 'Tennis'), ('Motorsports', 'Motorsports'), ('Science', 'Science'), ('Space', 'Space'), ('Biology', 'Biology'), ('Physics', 'Physics'), ('Environmental Science', 'Environmental Science'), ('Culture', 'Culture'), ('Art', 'Art'), ('History', 'History'), ('Literature', 'Literature'), ('Philosophy', 'Philosophy'), ('Education', 'Education'), ('Higher Education', 'Higher Education'), ('Online Learning', 'Online Learning'), ('Career Advice', 'Career Advice'), ('Academic Research', 'Academic Research'), ('Opinion', 'Opinion'), ('Editorials', 'Editorials'), ('Op-Eds', 'Op-Eds'), ('Letters to the Editor', 'Letters to the Editor'), ('Automotive', 'Automotive'), ('Car Reviews', 'Car Reviews'), ('Auto Industry News', 'Auto Industry News'), ('Maintenance Tips', 'Maintenance Tips'), ('Motorcycles', 'Motorcycles'), ('Home & Garden', 'Home & Garden'), ('Interior Design', 'Interior Design'), ('Gardening', 'Gardening'), ('DIY Projects', 'DIY Projects'), ('Home Improvement', 'Home Improvement'), ('Personal Finance', 'Personal Finance'), ('Investing', 'Investing'), ('Banking', 'Banking'), ('Insurance', 'Insurance'), ('Mental Health', 'Mental Health'), ('Medical News', 'Medical News'), ('Nutrition', 'Nutrition'), ('Fitness', 'Fitness'), ('Domestic Politics', 'Domestic Politics'), ('International Relations', 'International Relations'), ('Political Analysis', 'Political Analysis'), ('Policy', 'Policy'), ('Innovations', 'Innovations'), ('Scientific Discoveries', 'Scientific Discoveries'), ('Tech Reviews', 'Tech Reviews'), ('Space Exploration', 'Space Exploration'), ('Climate Change', 'Climate Change'), ('Conservation', 'Conservation'), ('Sustainability', 'Sustainability'), ('Wildlife', 'Wildlife'), ('Religious News', 'Religious News'), ('Spiritual Guidance', 'Spiritual Guidance'), ('Faith Discussions', 'Faith Discussions'), ('Theology', 'Theology'), ('Video Games', 'Video Games'), ('Board Games', 'Board Games'), ('Game Reviews', 'Game Reviews'), ('eSports', 'eSports'), ('Pregnancy', 'Pregnancy'), ('Child Development', 'Child Development'), ('Parenting Tips', 'Parenting Tips'), ('Family Activities', 'Family Activities')], max_length=50)),
                ('tag', models.CharField(choices=[('Technology', 'Technology'), ('Gadgets', 'Gadgets'), ('Software', 'Software'), ('AI', 'AI'), ('Startups', 'Startups'), ('Health', 'Health'), ('Fitness', 'Fitness'), ('Travel', 'Travel'), ('Food', 'Food'), ('Fashion', 'Fashion'), ('Entertainment', 'Entertainment'), ('Movies', 'Movies'), ('Music', 'Music'), ('Sports', 'Sports'), ('Finance', 'Finance'), ('Economy', 'Economy'), ('Business', 'Business'), ('Science', 'Science'), ('Space', 'Space'), ('Physics', 'Physics'), ('Biology', 'Biology'), ('Environment', 'Environment'), ('Art', 'Art'), ('History', 'History'), ('Philosophy', 'Philosophy'), ('Education', 'Education'), ('Career', 'Career'), ('Politics', 'Politics'), ('Opinion', 'Opinion'), ('Automotive', 'Automotive'), ('Home', 'Home'), ('Parenting', 'Parenting'), ('Gaming', 'Gaming'), ('Religion', 'Religion')], max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('page_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.blogpage')),
            ],
        ),
    ]
