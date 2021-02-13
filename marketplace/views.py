from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView

from .forms import CreateListingForm, Filter
from .models import Listing, Career


class Marketplace(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Listing
    template_name = 'marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filters'] = Filter()
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


class FilterListings(LoginRequiredMixin, ListView):
    template_name = 'marketplace/listings.html'
    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = Listing.objects.all()
        if self.request.GET.get('type') is not '' and self.request.GET.get('type') is not None:
            queryset = queryset.filter(type__istartswith=self.request.GET.get('type'))
        if self.request.GET.get('where') is not '' and self.request.GET.get('where') is not None:
            queryset = queryset.filter(where__istartswith=self.request.GET.get('where'))
        if self.request.GET.get('career') is not '' and self.request.GET.get('career') is not None:
            queryset = queryset.filter(career=int(self.request.GET.get('career')))

        return queryset

