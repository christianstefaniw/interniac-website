from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from accounts.models import User


def admin_required(func=None):
    def is_admin(obj):
        user = User.objects.get(id=obj.id)
        if not user.is_staff or not user.is_superuser:
            raise PermissionDenied
        return True

    actual_decorator = user_passes_test(is_admin)
    if func:
        return actual_decorator(func)
    else:
        return actual_decorator
