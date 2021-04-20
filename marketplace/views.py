from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required

from .forms import CreateListingForm, Filter
from .models import Listing, Career


__all__ = ['Marketplace', 'CreateListing', 'FilterListings', 'ViewListing', 'delete_listing', 'EditListing']


class Marketplace(LoginRequiredMixin, ListView):
    model = Listing
    ordering = ['-posted']
    template_name = 'marketplace/marketplace.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filters'] = Filter()

        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 15 or page_no <= 6:
            pages = [x for x in range(1, min(num_pages + 1, 16))]
        elif page_no > num_pages - 6:
            pages = [x for x in range(num_pages - 14, num_pages + 1)]
        else:
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
        return context


class CreateListing(LoginRequiredMixin, CreateView):
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
            return redirect('error')


class FilterListings(LoginRequiredMixin, ListView):
    template_name = 'marketplace/listings.html'
    model = Listing
    queryset = Listing.objects.all().order_by('-posted')
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        query = Q()
        params = self.request.GET
        if params.getlist('type'):
            for i in range(len(params.getlist('type'))):
                query = query & Q(type__startswith=params.getlist('type')[i])
        if params.getlist('where'):
            for i in range(len(params.getlist('where'))):
                query = query & Q(where__startswith=params.getlist('where')[i])
        if params.getlist('career'):
            for i in range(len(params.getlist('career'))):
                query = query & Q(career_id=int(params.getlist('career')[i]))
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
def delete_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user != listing.company:
        raise PermissionError

    listing.delete()

    return redirect('listings')


class EditListing(LoginRequiredMixin, UpdateView):
    model = Listing
    template_name = 'marketplace/edit-listing.html'
    success_url = reverse_lazy('listings')

    fields = ['title', 'type', 'where', 'career', 'new_career', 'pay', 'time_commitment', 'location',
              'application_deadline', 'description', 'application_url']

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()

        if request.POST['where'] == 'Virtual':
            if request.POST['location'] != '' and request.POST['location'] is not None:
                request.POST['location'] = ''

        if request.POST['type'] == 'Unpaid':
            if request.POST['pay'] != '' and request.POST['pay'] is not None:
                request.POST['pay'] = ''

        if request.POST['career'] is not None and request.POST['career'] != '':
            if request.POST['new_career'] != '' and request.POST['new_career'] is not None:
                request.POST['new_career'] = ''

        return super().post(request, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data['where'] == 'In-Person':
            if form.cleaned_data['location'] == '' or form.cleaned_data['location'] is None:
                form.add_error('location', 'Must have a location')

        if form.cleaned_data['type'] == 'Paid':
            if form.cleaned_data['pay'] == '' or form.cleaned_data['pay'] is None:
                form.add_error('pay', 'Paid internship must have a salary')

        if form.cleaned_data['career'] is None or form.cleaned_data['career'] == '':
            if form.cleaned_data['new_career'] is not None and form.cleaned_data['new_career'] != '':
                new_career, _ = Career.objects.get_or_create(career=form.cleaned_data['new_career'])
                listing = form.save(commit=False)
                listing.career = new_career
                listing.save()

        if form.is_valid():
            return super(EditListing, self).form_valid(form)
        else:
            return super(EditListing, self).form_invalid(form)
