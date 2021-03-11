class EmployerRequiredMixin:
    def get_context_data(self, **kwargs):
        if not self.request.user.is_employer:
            raise PermissionError
        return super(EmployerRequiredMixin, self).get_context_data(**kwargs)
