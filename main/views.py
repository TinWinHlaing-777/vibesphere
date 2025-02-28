from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm, BlogPageForm, ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Article, BlogPage
from django.contrib.auth.models import User
from django.contrib import messages

PROHIBITED_KEYWORDS = [
    'sexual', 'violence', 'political', 'terrorism', 'hate speech', 'explicit',
    'abuse', 'harassment', 'drug abuse', 'crime', 'scandal',
    'assault', 'murder', 'rape', 'bullying', 'intimidation',
    'extremism', 'bigotry', 'discrimination', 'x-rated', 'graphic content',
    'obscenity', 'profanity', 'vulgarity', 'offensive', 'disturbing',
    'insult', 'degradation', 'self-harm', 'suicide', 'addiction',
    'exploitation', 'brutality', 'gore', 'corruption', 'hate crime',
    'violence against women', 'racism', 'sexism', 'child abuse',
    'domestic violence', 'terrorist attack', 'hate group', 'radicalism',
    'cyberbullying', 'human trafficking', 'torture', 'trauma',
    'harsh language', 'illegal activity', 'abusive language', 'derogatory',
    'graphic violence', 'explicit content', 'adult content', 'mutilation',
    'incest', 'pedophilia', 'sadism', 'masochism', 'bully',
    'gang violence', 'sexual harassment', 'sexual assault', 'hate speech',
    'racial slur', 'religious intolerance', 'xenophobia', 'antisemitism',
    'homophobia', 'transphobia', 'violence towards animals', 'eco-terrorism',
    'genocide', 'war crimes', 'state violence', 'ethnic cleansing',
    'medical malpractice', 'eugenics', 'slavery', 'forced labor',
    'hate-mongering', 'dehumanization', 'victim blaming', 'mental abuse',
    'bullying behavior', 'persecution', 'forced marriage', 'reproductive abuse',
    'climate denial', 'human rights violations', 'child exploitation', 'hazing',
    'gaslighting', 'sexual exploitation', 'militant extremism', 'police brutality',
    'unethical experimentation', 'human rights abuses', 'terrorist propaganda',
    'mass incarceration', 'wage theft', 'censorship abuse', 'coercion',
    'unlawful detention', 'illegal surveillance', 'privacy invasion',
    'hate-fueled rhetoric', 'oppression', 'authoritarianism', 'surveillance abuse',
    'psychological torture', 'public shaming', 'intellectual property theft',
    'cyberstalking', 'revenge porn', 'exploitative content', 'non-consensual',
    'cultural appropriation', 'victimization', 'forced sterilization',
    'racial profiling', 'exclusionary practices', 'aggressive proselytizing',
    'manipulation', 'hostile work environment', 'unfair treatment'
]

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
    if request.method == 'POST':
        query = request.POST.get('query')
        categories = Article.objects.values_list('category', flat=True).distinct()
        
        if query:  
            articles = Article.objects.filter(category=query)
        else:
            articles = Article.objects.all()
        context = {
        'query':query,
        'show_navbar': True,
        'articles': articles,
        'categories': categories,
        }
        return render(request, 'articles.html', context)
    else:
        categories = Article.objects.values_list('category', flat=True).distinct()
        latest_articles = Article.objects.order_by('-view_count')[:5]
        latest_article = Article.objects.order_by('-created_date').first()
        articles = Article.objects.all()
        context = {
        'show_navbar': True,
        'latest_articles': latest_articles,
        'latest_article': latest_article,
        'articles': articles,
        'categories': categories,
        }
    return render(request, 'welcome.html', context)


def show_all_pages(request):
    pages = BlogPage.objects.all()
    context = {
        'show_navbar': True,
        'pages': pages
    }
    return render(request, 'pages.html', context)

@login_required
def create_update_blog_page(request, title=None):
    # Redirect if the user is not logged in
    redirect_response = redirect_if_not_logged_in(request)
    if redirect_response:
        return redirect_response

    # Determine if we are editing an existing page or creating a new one
    if title:
        page = get_object_or_404(BlogPage, title__iexact=title.lower(), author=request.user)
        is_editing = True
    else:
        page = None
        is_editing = False

    if request.method == 'POST':
        form = BlogPageForm(request.POST, request.FILES, instance=page, is_editing=is_editing)
        if form.is_valid():
            new_title = form.cleaned_data['title']

            # Check for prohibited content
            content = form.cleaned_data.get('meta_description', '')
            if any(keyword.lower() in content.lower() for keyword in PROHIBITED_KEYWORDS):
                messages.error(request, "Your description contains prohibited words or phrases and cannot be published.")
                return redirect('create_page', title=page.title if page else None)

            # Handle title change without creating a new page
            if is_editing and new_title.lower() != page.title.lower():
                if BlogPage.objects.filter(title__iexact=new_title.lower()).exists():
                    messages.error(request, 'A page with this title already exists.')
                    return redirect('create_page', title=page.title)
                page.title = new_title

            # Save the page
            blog_page = form.save(commit=False)
            if not is_editing:
                blog_page.author = request.user  # Set the author only if creating a new page
            blog_page.save()

            messages.success(request, 'Page updated successfully.' if is_editing else 'Page created successfully.')
            return redirect('pages')

    else:
        form = BlogPageForm(instance=page, is_editing=is_editing)

    context = {
        'show_navbar': True,
        'form': form,
        'page': page,
        'is_editing': is_editing,
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
def create_update_article(request, article_title=None):
    # Redirect if the user is not logged in
    redirect_response = redirect_if_not_logged_in(request)
    if redirect_response:
        return redirect_response

    blog_pages = BlogPage.objects.filter(author=request.user)
    if not blog_pages.exists():
        return redirect('create_page') 

    if article_title:
        article = get_object_or_404(Article, title=article_title, page_name__in=blog_pages)
        is_editing = True
    else:
        article = None
        is_editing = False

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle deletion
            if article:
                article.delete()
            return redirect('show_all_articles')
        
        form = ArticleForm(request.POST, request.FILES, instance=article, user=request.user, is_editing=is_editing)
        if form.is_valid():
            content = form.cleaned_data.get('content', '')

            # Check for prohibited content
            if any(keyword.lower() in content.lower() for keyword in PROHIBITED_KEYWORDS):
                messages.error(request, "Your content contains prohibited words or phrases and cannot be published.")
                return redirect('create') 
            
            article = form.save(commit=False)
            article.author = request.user  # Set the author
            article.save()  # Save the article
            return redirect('show_all_articles')
    else:
        form = ArticleForm(instance=article, user=request.user, is_editing=is_editing)
    
    context = {
        'show_navbar': True,
        'form': form,
        'articles': Article.objects.filter(page_name__in=blog_pages),
        'is_editing': is_editing,
        'article': article,
    }
    return render(request, 'create_article.html', context)



def show_all_articles(request):
        if request.method == 'POST':
            query = request.POST.get('query')
            categories = Article.objects.values_list('category', flat=True).distinct()
            
            if query:  
                articles = Article.objects.filter(category=query)
            else:
                articles = Article.objects.all()
            context = {
            'query':query,
            'show_navbar': True,
            'articles': articles,
            'categories': categories,
            }
            return render(request, 'articles.html', context)
        else:
            categories = Article.objects.values_list('category', flat=True).distinct()
            articles = Article.objects.all().order_by('-created_date')
            context = {
                'show_navbar': True,
                'articles': articles,
                'is_by_page': False,
                'categories': categories,
            }
        return render(request, 'articles.html', context)

@login_required
def read_article(request, id):
    article = get_object_or_404(Article, title=id)
    suggested_articles = Article.objects.order_by('-view_count')[:6]
    article.view_count += 1
    article.save(update_fields=['view_count'])
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('read_article', id=id)
    else:
        form = CommentForm()
    context = {
        'show_navbar': True,
        'article': article,
        'suggested_articles': suggested_articles,
        'form': form,
    }
    return render(request, 'read_article.html', context)

@login_required
def like_article(request, article_title):
    article = get_object_or_404(Article, title=article_title)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('read_article', id=article.title)

@login_required
def increment_share_count(request, article_title):
    article = get_object_or_404(Article, title=article_title)
    article.share_count += 1
    article.save()
    return JsonResponse({'share_count': article.share_count})

@login_required
def articles_by_page(request, page_name):
    page = get_object_or_404(BlogPage, title=page_name)
    articles = Article.objects.filter(page_name=page)

    context = {
        'show_navbar': True,
        'page': page,
        'articles_by_page': articles,
        'is_by_page': True,
    }
    return render(request, 'articles.html', context)