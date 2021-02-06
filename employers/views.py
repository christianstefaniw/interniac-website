from django.views.generic import TemplateView


class EmployersPage(TemplateView):
    template_name = 'employers/employers.html'
