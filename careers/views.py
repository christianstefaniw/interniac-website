from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView

from .models import Career
from mixins.admin_required import AdminRequiredMixin
from decorators.admin_required import admin_required

"""
Views for the careers app  
Currently we support the following views:

1. **`CareersPage`** - Renders all of the careers
2. **`EditCareer`** - Editing an existing career
3. **`delete_career`** - Delete a career
"""


class CareersPage(ListView):
    template_name = 'careers/careers.html'
    ordering = ['posted']
    model = Career


class EditCareer(AdminRequiredMixin, UpdateView):
    template_name = 'careers/edit-career.html'
    model = Career
    fields = ['content']


@admin_required
def delete_career(request, career_id):
    career = Career.objects.get(id=career_id)
    career.delete()
    return redirect('success')
