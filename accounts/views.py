from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.core.checks import messages
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm
from django.contrib.auth import login as auth_login

# FBV 함수 기반 뷰
'''
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 로그인처리
            # auth_login(request, user)
            next_url = request.GET.get('next') or 'profile'
            # return redirect(next_url)

            
            # return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })
'''


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect(self.get_success_url())


# CBV 클라스 기반 뷰
signup = SignupView.as_view()


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_form.html'
    # email_template_name = ...
    #html_email_template_name = ...
    def form_valid(self, form):
        messages.info(self.request, '암호 변경 메일을 발송했습니다.')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 리셋을 완료했습니다.')
        return super().form_valid(form)
