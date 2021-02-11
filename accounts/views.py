from django.shortcuts import render

from .forms import StudentProfileForm
from .models import StudentProfile


def profile(request):
    if request.user.is_student:
        return Student.student_profile(request)
    return render(request, template_name='accounts/profile.html')


class Student:

    @staticmethod
    def student_profile(request):
        context = {}
        student_form = Student.create_student_form(request)
        if request.method == 'POST':
            if student_form.is_valid():
                student_form.save()

        context.update({'student_profile_form': student_form})
        return render(request, template_name='accounts/profile.html', context=context)

    @staticmethod
    def create_student_form(request):
        if request.method == 'POST':
            instance = StudentProfile.objects.get(user=request.user)
            form = StudentProfileForm(request.POST, instance=instance)
            current_data = StudentProfile.objects.get(user=request.user)
        else:
            form = StudentProfileForm()
            current_data = StudentProfile.objects.get(user=request.user)

        for i, field in enumerate(current_data.__dict__):
            if field == '_state' or field == 'user_id':
                continue
            else:
                form[field].initial = current_data.__dict__[field]

        return form
