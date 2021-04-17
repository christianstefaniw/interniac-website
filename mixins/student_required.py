from django.contrib.auth.mixins import AccessMixin

class StudentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionError
        if not request.user.is_student:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
