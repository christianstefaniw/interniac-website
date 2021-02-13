from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView

from .forms import CreateListingForm
from .models import Listing


class Marketplace(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['all_listings'] = Listing.objects.all()
        return context


class CreateListing(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'marketplace/create-listing.html'
    form_class = CreateListingForm

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.org = self.request.user
            obj.save()
            return HttpResponseRedirect('/success')
        else:
            return HttpResponseRedirect('/error')