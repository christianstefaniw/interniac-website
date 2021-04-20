from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView
from django.core.exceptions import PermissionDenied

from careers.models import Career


class CareersPage(ListView):
    template_name = 'careers/careers.html'
    model = Career


class EditCareer(UpdateView):
    template_name = 'careers/edit-career.html'
    model = Career
    fields = ['content']


def delete_career(request, career_id):
    if request.user.is_staff or request.user.is_superuser:
        career = Career.objects.get(id=career_id)
        career.delete()
        return redirect('success')
    else:
        raise PermissionDenied
