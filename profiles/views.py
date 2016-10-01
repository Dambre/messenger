from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, UserCreationForm


class LoginView(View):
    template_name = 'profiles/login.html'    

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form  = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    template_name = 'profiles/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')