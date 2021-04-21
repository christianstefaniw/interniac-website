from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class StudentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student:
            raise PermissionDenied
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
