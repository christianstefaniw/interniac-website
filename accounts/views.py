from django.views.generic import TemplateView

from .forms import StudentProfileForm
from .models import StudentProfile


class Profile(TemplateView):
    template_name = 'accounts/profile.html'

    def student_form(self):
        form = StudentProfileForm()
        current_data = StudentProfile.objects.get(user=self.request.user)
        for i, field in enumerate(current_data.__dict__):
            if field == '_state' or field == 'user_id':
                continue
            else:
                form[field].initial = current_data.__dict__[field]
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['student_profile_form'] = self.student_form()
        return context
