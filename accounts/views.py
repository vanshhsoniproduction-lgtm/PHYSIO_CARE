from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('appointments:home')

    login_form = LoginForm()
    signup_form = SignupForm()
    active_tab = 'login'

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('appointments:home')
            else:
                active_tab = 'login'
        
        elif form_type == 'signup':
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('appointments:home')
            else:
                active_tab = 'signup'

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'active_tab': active_tab
    }
    return render(request, 'accounts/auth.html', context)

def logout_view(request):
    logout(request)
    return redirect('accounts:auth')
