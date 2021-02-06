from django.views.generic import TemplateView

class StudentsPage(TemplateView):
    template_name = 'students/students.html'
