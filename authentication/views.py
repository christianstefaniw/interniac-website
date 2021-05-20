from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UserCreateForm

"""
Views for the authentication app  
Currently we support the following view:

1. **`Register`** - Creates an account for a client
"""


class Register(FormView):
    template_name = 'auth/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """
        This method overrides `FormView`'s `form_valid` method to log the user in as soon as they register
        """
        valid = super(Register, self).form_valid(form)
        new_user = form.save()
        login(self.request, new_user)
        return valid
