from django.views.generic import TemplateView
from django.utils.timezone import now


class BaseView(TemplateView):
    template_name = 'src/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ano'] = now().year
        return context


class HomePartialView(TemplateView):
    template_name = 'src/home.html'
