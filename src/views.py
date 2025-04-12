from django.views.generic import TemplateView
from django.utils.timezone import now
from django.shortcuts import render
from django.views import View

class BaseView(TemplateView):
    #template_name = 'src/base.html'
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ano'] = now().year
        return context


class HomePartialView(TemplateView):
    #template_name = 'src/home.html'
    template_name = 'home.html'

