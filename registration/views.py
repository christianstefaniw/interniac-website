from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView

from .forms import UserCreateForm


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        valid = super(Register, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(username=email, password=password)
        login(self.request, new_user)
        return valid
