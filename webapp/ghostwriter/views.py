import os
from subprocess import Popen
from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.conf import settings
from time import sleep
from .models import Image, Lecture, TaskRecord, TaskState, TaskType
from .forms import LectureForm, LectureImageRelForm
from .tasks import get_ocr_text, empty_task, register_image


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
        obj_ids = request.POST.getlist("images")
        # get_ocr_text.delay(lec_id, obj_ids)
        return redirect("ghostwriter:lecture", id=2)


class LectureView(ListView):
    template_name = 'ghostwriter/lectures.html'
    model = Lecture


class LectureDetailView(TemplateView):
    template_name = 'ghostwriter/lecture_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LectureDetailView, self).get_context_data(**kwargs)
        lec_id = self.kwargs['id']
        lec = Lecture.objects.get(id=lec_id)
        from .capture_lib import QuestionGenerator
        question_gen = QuestionGenerator(goolab_api_key=settings.GOOLAB_API_ID, text=lec.ocr_text)
        context['item'] = lec
        context['questions'] = question_gen
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
        lec = Lecture.objects.get(id=lec_id)
        context['item'] = lec
        from .capture_lib import QuestionGenerator
        question_gen = QuestionGenerator(goolab_api_key=settings.GOOLAB_API_ID, text=lec.ocr_text)
        context['questions'] = question_gen.get_questions(max_questions=3)
        return context


class CameraCalibration(TemplateView):
    template_name = "ghostwriter/calibrate.html"

    def post(self, request, *args, **kwards):
        task_id = empty_task.delay().id
        TaskRecord.objects.create(
            state=TaskState.RUNNING.value,
            type=TaskType.CAPTURE.value,
            task_id=task_id
        )
        # p = Popen("python manage.py capture", shell=True, close_fds=False)
        # with open("process.pid", "w") as fp:
        #     fp.write(str(p.pid))
        return redirect("ghostwriter:tasks")


class TaskView(TemplateView):
    template_name = "ghostwriter/task_abstract.html"

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        context["tasks"] = TaskRecord.objects.all().order_by('-id')
        return context

    def post(self, request, *args, **kwards):
        task_id = request.POST.get("task_id")
        task_record = TaskRecord.objects.get(task_id=task_id)
        try:
            # with open("process.pid", "r") as fp:
            #     from signal import SIGINT
            #     pid = fp.read()
            # os.kill(int(pid), SIGINT)
            task_record.state = TaskState.DONE.value
            # register_image.delay()
            sleep(1)
            return redirect('ghostwriter:index')
        except Exception as e:
            print(e.args)
            task_record.state = TaskState.FAIL.value
            return redirect('ghostwriter:tasks')
        finally:
            task_record.save()
