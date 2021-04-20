from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class StudentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student or not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
