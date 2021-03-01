from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required

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
            new_listing.company = self.request.user
            if new_listing.career_id is None:
                new_career, _ = Career.objects.get_or_create(career=new_listing.new_career)
                new_listing.career = new_career
            new_listing.save()
            return render(self.request, 'success-error/success-created-listing.html', context={'listing': new_listing})
        else:
            return redirect(reverse('error'))


class FilterListings(LoginRequiredMixin, ListView):
    template_name = 'marketplace/listings.html'
    model = Listing

    def get_queryset(self):
        queryset = super().get_queryset()
        query = Q()
        params = self.request.GET
        if params.getlist('type'):
            for i in range(len(params.getlist('type'))):
                query = query | Q(type__startswith=params.getlist('type')[i])
        if params.getlist('where'):
            for i in range(len(params.getlist('where'))):
                query = query | Q(where__startswith=params.getlist('where')[i])
        if params.getlist('career'):
            for i in range(len(params.getlist('career'))):
                query = query | Q(career_id=int(params.getlist('career')[i]))
        if params.get('search'):
            query = query & Q(title__contains=params.get('search'))
        if params.get('company'):
            query = query & Q(company=params.get('company'))

        queryset = queryset.filter(query)

        return queryset


class ViewListing(LoginRequiredMixin, DetailView):
    model = Listing
    template_name = 'marketplace/single-listing.html'


@login_required
def apply(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.applications.add(request.user)
    redirect_where = request.GET.get('redirect')
    if redirect_where == 'profile':
        return redirect(request.user)
    elif redirect_where == 'success':
        return render(request, 'success-error/success-applied.html', context={'which': listing})
    else:
        return HttpResponse(f'<button class="apply-unapply-btn" onclick="unapply({listing_id}, this)">Unapply</button>')


@login_required
def unapply(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.applications.remove(request.user)
    redirect_where = request.GET.get('redirect')
    if redirect_where == 'profile':
        return redirect('applications')
    elif redirect_where == 'success':
        return render(request, 'success-error/success-unapplied.html', context={'which': listing})
    else:
        return HttpResponse(f'<button class="apply-unapply-btn" onclick="apply({listing_id}, this)">Apply</button>')


@login_required
def delete_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user != listing.company:
        raise PermissionError

    listing.delete()

    return redirect(reverse('listings'))


class EditListing(LoginRequiredMixin, UpdateView):
    model = Listing
    template_name = 'marketplace/edit-listing.html'
    success_url = reverse_lazy('listings')
    fields = ['title', 'type', 'where', 'career', 'new_career', 'time_commitment', 'application_deadline',
              'description', 'application_url']
