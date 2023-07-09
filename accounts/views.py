from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import SignInForm


class SignIn(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = SignInForm()
        context = dict()
        context['form'] = form
        return render(request, 'accounts/sign_in.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = SignInForm(request, request.POST)
        context = dict()
        context['form'] = form

        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('home')

        return render(request, 'accounts/sign_in.html', context)


class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect('home')
