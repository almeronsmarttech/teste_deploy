from django.views.generic import TemplateView
from django.utils.timezone import now
from django.shortcuts import render
from django.views import View
import os
import random
from django.conf import settings



class BaseView(TemplateView):
    #template_name = 'src/base.html'
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ano'] = now().year
        return context


class HomePartialView(TemplateView):
    ##template_name = 'src/home.html'
    template_name = 'home.html'

#class HomePartialView(TemplateView):
#    template_name = "home_partial.html"

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)

#        pasta = os.path.join(settings.STATICFILES_DIRS[0], "imagens")
#        imagens_disponiveis = [
#            img for img in os.listdir(pasta)
#            if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
#        ]

#        context["imagens"] = random.sample(imagens_disponiveis, 4) if len(imagens_disponiveis) >= 4 else imagens_disponiveis
#        return context