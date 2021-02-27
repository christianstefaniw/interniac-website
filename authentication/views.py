from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UserCreateForm


class Register(FormView):
    template_name = 'auth/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        valid = super(Register, self).form_valid(form)
        new_user = form.save()
        login(self.request, new_user)
        return valid
