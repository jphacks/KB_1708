from django.views.generic import TemplateView,ListView
from .models import Image,Lecture


class IndexView(TemplateView):
    template_name = "ghostwriter/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["object_list"] = Image.objects.filter(lecture__isnull=True).all()
        return context

class LectureView(ListView):
    template_name = 'ghostwriter/lectures.html'
    model = Lecture

class LectureDetailView(TemplateView):
    template_name = 'ghostwriter/lecture_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LectureDetailView, self).get_context_data(**kwargs)
        lec_id = self.kwargs['id']
        context['item'] = Lecture.objects.get(id=lec_id)
        return context
