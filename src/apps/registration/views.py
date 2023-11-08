from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.registration.forms import RegistrationForm


class RegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form: RegistrationForm) -> HttpResponseRedirect:
        cd = form.cleaned_data
        user = form.save(commit=False)
        user.set_password(cd['password'])
        user.save()
        login(
            self.request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return redirect('/')
