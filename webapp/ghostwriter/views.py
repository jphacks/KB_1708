from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Image, Lecture
from .forms import LectureForm, LectureImageRelForm


class IndexView(TemplateView):
    template_name = "ghostwriter/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        form = LectureImageRelForm()
        context["object_list"] = Image.objects.filter(lecture__isnull=True).all()
        context['form'] = form
        return context

    def post(self, request, *args, **kwards):
        lec_id = request.POST["lecture"]
        lecture = Lecture.objects.get(id=lec_id)
        obj_ids = request.POST.getlist("images")
        ocr_text = ""
        for i in obj_ids:
            image = Image.objects.get(id=i)
            image.lecture = lecture
            ocr_text += image.ocr
            image.save()
        lecture.ocr_text = ocr_text
        lecture.save()
        return redirect("ghostwriter:index")


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


class LectureCreateView(CreateView):
    model = Lecture
    template_name = 'ghostwriter/lecture_create.html'
    form_class = LectureForm
    success_url = reverse_lazy("ghostwriter:lectures")


class LectureQuestionView(TemplateView):
    template_name = "ghostwriter/lecture_question.html"

    def get_context_data(self, **kwargs):
        context = super(LectureQuestionView, self).get_context_data(**kwargs)
        lec_id = self.kwargs["id"]
        context['item'] = Lecture.objects.get(id=lec_id)
        context['questions'] = ["Q1. 今は何時でしょう",
                                "Q2. タクシオくんのissueはあと3つ残っています．タクシオくんが朝までに寝れる確率を答えなさい",
                                "Q3. このハッカソンを通じて成長したたつやくんの成長率を求めよ．"]
        return context

