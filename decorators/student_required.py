from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from accounts.models import User


def student_required(func=None):
    def is_student(obj):
        if not User.objects.get(id=obj.id).is_student:
            raise PermissionDenied
        return True

    actual_decorator = user_passes_test(is_student)
    if func:
        return actual_decorator(func)
    else:
        return actual_decorator
