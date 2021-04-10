from django.contrib.auth.decorators import user_passes_test

from accounts.models import User


def employer_required(func=None):
    def is_employer(obj):
        if not User.objects.get(id=obj.id).is_employer:
            raise PermissionError
        return True

    actual_decorator = user_passes_test(is_employer)
    if func:
        return actual_decorator(func)
    else:
        return actual_decorator
