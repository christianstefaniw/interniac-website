from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from mixins.admin_required import AdminRequiredMixin
from careers.models import Career
from accounts.models import User
from decorators.admin_required import admin_required


class CareerInfoFormView(AdminRequiredMixin, CreateView):
    template_name = 'interniac-admin/new-career.html'
    model = Career
    fields = ['content']
    success_url = reverse_lazy('success')

class AllUsers(AdminRequiredMixin, ListView):
    model = User
    paginate_by = 30
    template_name = 'interniac-admin/all-users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

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

class UserInfo(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'interniac-admin/user-info/user-info.html'

@login_required
@admin_required
def delete_account(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(reverse('success'))