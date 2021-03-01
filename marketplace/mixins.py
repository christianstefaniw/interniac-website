from django.forms import modelform_factory


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)