from django.views.generic import TemplateView
from .models import Image


class IndexView(TemplateView):
    template_name = "ghostwriter/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["object_list"] = Image.objects.filter(lecture__isnull=True).all()
        return context
