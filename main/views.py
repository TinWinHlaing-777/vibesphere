from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm, BlogPageForm, ArticleForm
from django.contrib.auth.decorators import login_required
from .models import Article, BlogPage
from django.contrib.auth.models import User
from django.contrib import messages

# Create Account Function
def register_view(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('welcome')
            else:
                form_errors = form.errors
        else: 
            form = CustomUserCreationForm()
            form_errors = None
        context = {
            'show_navbar': False,
            'form': form,
            'form_errors': form_errors
        }
        return render(request, 'register.html', context)


# Login Function
def login_view(request): 
    if request.method == 'POST':
         form = CustomLoginForm(request, data = request.POST)
         if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('welcome')
    else: 
        form = CustomLoginForm()
    context = {
        'show_navbar': False,
        'form': form,
    }
    return render(request, 'login.html', context)

# Logout function
def logout_view(request):
     logout(request)
     return redirect('login')

def redirect_if_not_logged_in(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return None

# View Overall Function
# @login_required
def welcome_view(request):
        context = {'show_navbar': True}
        return render(request, 'welcome.html', context)

def show_all_pages(request):
    pages = BlogPage.objects.all()
    context = {
        'show_navbar': True,
        'pages': pages
    }
    return render(request, 'pages.html', context)


@login_required
def blog_page_create(request):
    redirect_response = redirect_if_not_logged_in(request)
    if redirect_response:
        return redirect_response
    if request.method == 'POST':
        form = BlogPageForm(request.POST, request.FILES)
        if form.is_valid():
            blog_page = form.save(commit=False)
            blog_page.author = request.user
            blog_page.save()             
            return redirect('pages')
    else:
        form = BlogPageForm()
    context = {
        'show_navbar': True,
        'form': form
        }
    return render(request, 'page_form.html', context)

@login_required
def manage_page(request, user_id=None):
    redirect_response = redirect_if_not_logged_in(request)
    if redirect_response:
        return redirect_response
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        messages.error(request,'No user specified')
        return redirect('welcome')
    pages = BlogPage.objects.filter(author=user)

    if pages.exists():
        if pages.count() > 1:
            messages.warning(request, 'Multiple pages found. Showing the first page.')
        page = pages.first()  
        return redirect('update_page', title=page.title)
    else:
        messages.info(request, 'You do not have a page. Please create a new page.')
        return redirect('create_page')
    
@login_required
def update_page(request, title):
    redirect_response = redirect_if_not_logged_in(request)
    if redirect_response:
        return redirect_response
    page = get_object_or_404(BlogPage, title__iexact=title.lower())
    if page.author != request.user:
        messages.error(request, 'You do not have permission to edit this page.')
        return redirect('create_page')
    if request.method == 'POST':
        if 'delete_page' in request.POST:
            page.delete()
            messages.success(request, 'Page deleted successfully.')
            return redirect('pages') 
        else:
            form = BlogPageForm(request.POST, request.FILES, instance=page)
            if form.is_valid():
                form.save()
                messages.success(request, 'Page updated successfully.')
                return redirect('pages')  
    else:
        form = BlogPageForm(instance=page)
    context = {
        'show_navbar': True,
        'form': form,
        'page': page
    }
    return render(request, 'page_form.html', context)
    
@login_required
def create_update_article(request, article_id=None):
    redirect_response = redirect_if_not_logged_in(request)
    if redirect_response:
        return redirect_response
    blog_page = get_object_or_404(BlogPage, author=request.user)
    articles = Article.objects.filter(page_name=blog_page)
    if article_id:
        article = Article.objects.get(pk=article_id)
    else:
        article = None
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            blog_page = form.save(commit=False)  
            blog_page.author = request.user  
            blog_page.save()  
            return redirect('welcome')
    else:
        form = ArticleForm(instance=article)
    context = {
        'show_navbar': True,
        'form': form,
        'articles': articles
    }
    return render(request, 'create_article.html', context)

def show_all_articles(request):
    articles = Article.objects.all()
    context = {
        'show_navbar': True,
        'articles': articles,
    }
    return render(request, 'articles.html', context)

def read_article(request, id):
    article = get_object_or_404(Article, title=id)
    suggested_articles = Article.objects.all()
    context = {
        'show_navbar': True,
        'article': article,
        'suggested_articles': suggested_articles,
    }
    return render(request, 'read_article.html', context)





