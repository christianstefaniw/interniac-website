from django.views.generic import TemplateView


class AboutUsPage(TemplateView):
    template_name = 'aboutus/aboutus.html'
