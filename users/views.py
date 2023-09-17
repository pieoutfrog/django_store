from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from users.forms import UserRegisterForm, UserProfileForm
from users.services import send_verification_email, send_password


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        verification_token = get_random_string(length=15)
        form.instance.verification_token = verification_token
        send_verification_email(form.instance.email, verification_token)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:verification_email')


class VerifyEmailView(View):
    template_name = 'users/verification_email.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        User = get_user_model()
        try:
            user = User.objects.get(verification_token=verification_code)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect('users:confirmation_success')
        except User.DoesNotExist:
            pass
        return redirect('users:confirmation_error')


class ConfirmationSuccessView(TemplateView):
    template_name = 'users/confirmation_success.html'


class ConfirmationErrorView(TemplateView):
    template_name = 'users/confirmation_error.html'


class CreationErrorView(TemplateView):
    template_name = 'users/password_reset_success.html'


class ConfirmEmailView(View):

    def get(self, request, token):
        User = get_user_model()

        try:
            user = User.objects.get(verification_token=token)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return render(request, 'confirmation_success.html')

        except User.DoesNotExist:
            return render(request, 'confirmation_error.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = PasswordChangeForm
    success_url = '/users/profile/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Ваш пароль успешно изменен.')
        return super().form_valid(form)


class GenerateAndSendPasswordView(View):
    template_name = 'users/generate_and_send_password.html'
    form = PasswordResetForm()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        self.form = PasswordResetForm(request.POST)
        if self.form.is_valid():
            email = self.form.cleaned_data['email']
            if send_password(email):
                return render(request, 'users/password_reset_success.html', {'email': email})
        return render(request, 'users/password_reset_error.html')

