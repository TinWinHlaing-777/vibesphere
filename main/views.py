from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .models import User
from .forms import UserRegistrationForm, UserLoginForm


# Create Account Function
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('welcome')
    else:
        form = UserRegistrationForm()
    context = {
        'show_navbar': False,
        'form': form,
    }
    return render(request, 'register.html', context)

# Login Function
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email = email)
                if check_password(password, user.password):
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully!')
                    return redirect('welcome')
                else: 
                    messages.error(request, 'Invalid password!')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password!')
    else:
        form = UserLoginForm()
    context = {
        'show_navbar': False,
        'form': form,
    }
    return render(request, 'login.html', context)

# View Overall Function
def welcome_view(request):
    context = {'show_navbar': True}
    return render(request, 'welcome.html', context)

# View User Data On Profile Page
# def showUserData(request, user_id):
#     print(user_id)
    # user = User.objects.get(pk = user_id)
    # print(user)
    # if request.method == 'POST':
    #     image_form = ProfileImageForm(request.POST, request.FILES, instance=user)
    #     if image_form.is_valid():
    #         image_form.save()
    #         return redirect('profile', user_id=user_id)
    # else: 
    #     image_form = ProfileImageForm(instance=user)
    # context = {
    #     'show_navbar': True,
    #     'user': user,
        # 'image_form': image_form,
    # }
    # return render(request, 'profile.html', context)

