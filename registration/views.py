from django.views.generic import CreateView, FormView

from .forms import UserCreateForm


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = '/'

