from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import BlogPage, Article, Comment
from .forms import CustomUserCreationForm, CustomLoginForm, BlogPageForm, ArticleForm

class ModelTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        # Create a test BlogPage
        self.blog_page = BlogPage.objects.create(
            title='Test Blog Page',
            author=self.user,
            profile_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            meta_description='This is a test blog page.',
            status='published'
        )

        # Create a test Article
        self.article = Article.objects.create(
            title='Test Article',
            page_name=self.blog_page,
            author=self.user,
            article_image=SimpleUploadedFile(name='test_article_image.jpg', content=b'', content_type='image/jpeg'),
            content='This is a test article content.',
            category='Technology'
        )

        # Create a test Comment
        self.comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            content='This is a test comment.',
            approved=True
        )

    # Test BlogPage Model
    def test_blog_page_creation(self):
        self.assertEqual(self.blog_page.title, 'Test Blog Page')
        self.assertEqual(self.blog_page.author.username, 'testuser')
        self.assertEqual(self.blog_page.meta_description, 'This is a test blog page.')
        self.assertEqual(self.blog_page.status, 'published')
        self.assertTrue(self.blog_page.profile_image)  # Check if the image field is populated
        self.assertEqual(str(self.blog_page), 'Test Blog Page')  # Test __str__ method

    def test_blog_page_unique_title(self):
        with self.assertRaises(Exception):
            BlogPage.objects.create(
                title='Test Blog Page',  # Duplicate title
                author=self.user,
                profile_image=SimpleUploadedFile(name='test_image2.jpg', content=b'', content_type='image/jpeg'),
                meta_description='Another test blog page.',
                status='draft'
            )

    # Test Article Model
    def test_article_creation(self):
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.page_name.title, 'Test Blog Page')
        self.assertEqual(self.article.author.username, 'testuser')
        self.assertEqual(self.article.content, 'This is a test article content.')
        self.assertEqual(self.article.category, 'Technology')
        self.assertTrue(self.article.article_image)  # Check if the image field is populated
        self.assertEqual(str(self.article), 'Test Article')  # Test __str__ method

    def test_article_unique_title(self):
        with self.assertRaises(Exception):
            Article.objects.create(
                title='Test Article',  # Duplicate title
                page_name=self.blog_page,
                author=self.user,
                article_image=SimpleUploadedFile(name='test_article_image2.jpg', content=b'', content_type='image/jpeg'),
                content='Another test article content.',
                category='Science'
            )

    def test_article_category_choices(self):
        # Test valid category choice
        valid_article = Article.objects.create(
            title='Valid Category Article',
            page_name=self.blog_page,
            author=self.user,
            article_image=SimpleUploadedFile(name='test_article_image3.jpg', content=b'', content_type='image/jpeg'),
            content='This is a valid category article.',
            category='Science'
        )
        self.assertEqual(valid_article.category, 'Science')

        # Test invalid category choice
        invalid_article = Article(
            title='Invalid Category Article',
            page_name=self.blog_page,
            author=self.user,
            article_image=SimpleUploadedFile(name='test_article_image4.jpg', content=b'', content_type='image/jpeg'),
            content='This is an invalid category article.',
            category='Invalid Category'  # Invalid choice
        )
        with self.assertRaises(ValidationError):  # Expect a ValidationError
            invalid_article.full_clean()  # Validate the model instance

    def test_article_likes(self):
        # Test adding likes to an article
        self.assertEqual(self.article.likes.count(), 0)
        self.article.likes.add(self.user)
        self.assertEqual(self.article.likes.count(), 1)
        self.assertTrue(self.user in self.article.likes.all())

    # Test Comment Model
    def test_comment_creation(self):
        self.assertEqual(self.comment.article.title, 'Test Article')
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertTrue(self.comment.approved)
        self.assertEqual(str(self.comment), 'Comment by testuser on Test Article')  # Test __str__ method

    def test_comment_approval(self):
        # Test unapproved comment
        unapproved_comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            content='This is an unapproved comment.',
            approved=False
        )
        self.assertFalse(unapproved_comment.approved)


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.blog_page = BlogPage.objects.create(
            title='Test Page',
            author=self.user,
            profile_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            meta_description='This is a test blog page.',
            status='published'
        )
        self.article = Article.objects.create(
            title='Test Article',
            page_name=self.blog_page,
            author=self.user,
            article_image=SimpleUploadedFile(name='test_article_image.jpg', content=b'test content', content_type='image/jpeg'),  # Add valid content
            content='This is a test article content.',
            category='Technology'
        )

    # Test User Registration
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'email': 'newuser@example.com',  # Add email if required
        })
        self.assertEqual(response.status_code, 302)  # Redirects to 'welcome' on success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # Test User Login
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirects to 'welcome' on success

    # Test User Logout
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to 'login' on success

    # Test Welcome View
    def test_welcome_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome.html')

    # Test Create/Update Blog Page
    # def test_create_update_blog_page(self):
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get(reverse('create_page'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'page_form.html')

    #     response = self.client.post(reverse('create_page'), {
    #         'title': 'New Page',
    #         'meta_description': 'This is a new blog page without prohibited keywords.',
    #         'profile_image': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),  # Add profile_image
    #         'status': 'published',  # Add status
    #     })
    #     if response.status_code == 200:  # Form submission failed
    #         print("Form errors:", response.context['form'].errors)  # Print form errors for debugging
    #     self.assertEqual(response.status_code, 200)  # Form submission should return 200
    #     self.assertTrue(BlogPage.objects.filter(title='New Page').exists())

    # Test Manage Page
    def test_manage_page(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('manage_page', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to 'update_page' or 'create_page'

    # Test Create/Update Article
    # def test_create_update_article(self):
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get(reverse('create'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'create_article.html')

    #     response = self.client.post(reverse('create'), {
    #         'title': 'New Article',
    #         'content': 'This is a test article content without prohibited keywords.',
    #         'page_name': self.blog_page.title,  # Use title as the primary key
    #         'category': 'Technology',  # Add category
    #         'article_image': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),  # Add article_image
    #     })
    #     if response.status_code == 200:  # Form submission failed
    #         print("Form errors:", response.context['form'].errors)  # Print form errors for debugging
    #     self.assertEqual(response.status_code, 200)  # Form submission should return 200
    #     self.assertTrue(Article.objects.filter(title='New Article').exists())

    # Test Show All Articles
    def test_show_all_articles(self):
        response = self.client.get(reverse('show_all_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles.html')

    # Test Read Article
    def test_read_article(self):
        self.client.login(username='testuser', password='testpass123')  # Log in the user
        response = self.client.get(reverse('read_article', args=[self.article.title]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'read_article.html')

    # Test Like Article
    def test_like_article(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('like_article', args=[self.article.title]))
        self.assertEqual(response.status_code, 302)  # Redirects to 'read_article'

    # Test Increment Share Count
    def test_increment_share_count(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('increment_share_count', args=[self.article.title]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['share_count'], 1)

    # Test Articles By Page
    def test_articles_by_page(self):
        self.client.login(username='testuser', password='testpass123')  # Log in the user
        response = self.client.get(reverse('articles_by_page', args=[self.blog_page.title]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles.html')