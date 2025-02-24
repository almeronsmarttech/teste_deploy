from django.views.generic import TemplateView


class FormPartialView(TemplateView):
    template_name = 'loginapp/form.html'
