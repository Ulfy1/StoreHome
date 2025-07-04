from django.shortcuts import render, HttpResponseRedirect, redirect
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"Successfully login in {user} account")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Login',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)


            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"Account {user.username} was created!")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Home - Registration',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile was changed!")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserRegistrationForm(instance=request.user)

    context = {
        'title': 'Home - Profile',
        'form': form
    }

    return render(request, 'users/profile.html', context)

def users_cart(request):
    return render(request, 'users/users_cart.html')


@login_required
def logout(request):
    messages.success(request, f"Logout successfully")
    auth.logout(request)
    return redirect(reverse('main:index'))