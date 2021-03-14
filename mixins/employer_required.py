from django.contrib.auth.mixins import AccessMixin


class EmployerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_employer:
            raise PermissionError
        return super().dispatch(request, *args, **kwargs)
