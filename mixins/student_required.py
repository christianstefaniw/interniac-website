from django.contrib.auth.mixins import AccessMixin

class StudentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_student:
            raise PermissionError
        return super().dispatch(request, *args, **kwargs)
