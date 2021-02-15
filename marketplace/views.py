from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView

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
            new_listing = form.save(commit=False)
            new_listing.org = self.request.user
            if new_listing.career_id is None:
                new_career, _ = Career.objects.get_or_create(career=new_listing.new_career)
                new_listing.career = new_career
            new_listing.save()
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
        query = Q()
        if self.request.GET.getlist('type') is not None:
            for i in range(len(self.request.GET.getlist('type'))):
                query = query | Q(type__startswith=self.request.GET.getlist('type')[i])
        if self.request.GET.getlist('where') is not None:
            for i in range(len(self.request.GET.getlist('where'))):
                query = query | Q(where__startswith=self.request.GET.getlist('where')[i])
        if self.request.GET.getlist('career') is not None:
            for i in range(len(self.request.GET.getlist('career'))):
                query = query | Q(career_id=int(self.request.GET.getlist('career')[i]))

        queryset = queryset.filter(query)

        return queryset


def apply(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.applications.add(request.user)
    return redirect('/success')
