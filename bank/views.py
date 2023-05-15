from django.views.generic import TemplateView

from . import models


class SimpleTemplateView(TemplateView):
    template_name = "bank/simple_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_data'] = models.SimpleModel.objects.all()
        return context
