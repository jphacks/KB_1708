import os
from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.conf import settings
from .models import Image, Lecture, TaskRecord
from .forms import LectureForm, LectureImageRelForm
from .capture_lib import SlideCapture, SlideCaptureError


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
        images = []
        for i in obj_ids:
            image = Image.objects.get(id=i)
            image.lecture = lecture
            image.save()
            images.append(image)
        from .capture_lib import OcrWrapper
        ocr = OcrWrapper(settings.GCV_API_KEY)
        paths = [i.image.path for i in images]
        results = ocr.get_ocr_result(paths)
        for res, image in zip(results, images):
            text = ocr.get_ocr_string(res)
            image.ocr = text
            ocr_text += text
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
        lec = Lecture.objects.get(id=lec_id)
        context['item'] = lec
        from .capture_lib import GoolabWrapper
        goo = GoolabWrapper(settings.GOOLAB_API_ID)
        keywords = goo.get_keywords_from_ocr_string(lec.ocr_text)
        questions = goo.generate_selected_num_of_questions(keywords, 3)
        context['questions'] = questions
        return context


class CameraCalibration(TemplateView):
    template_name = "ghostwriter/calibrate.html"

    def get_context_data(self, **kwargs):
        context = super(CameraCalibration, self).get_context_data(**kwargs)
        tasks = TaskRecord.objects.filter(type=1).filter(state=0).all()
        for task in tasks:
            task.state = 1
            task.save()
        save_dir = os.path.join(settings.BASE_DIR, "media", "cache")
        context['capture_error'] = False
        try:
            with SlideCapture(1) as cap:
                cap.calibration(save_dir)
        except SlideCaptureError:
            context['capture_error'] = True
        return context

    def post(self, request, *args, **kwards):
        if request.POST.get('force_delete', None):
            from celery.task.control import revoke
            task = TaskRecord.objects.filter(type=1).filter(state=0).first()
            if task:
                revoke(task.task_id, terminate=True)
            return redirect("ghostwriter:tasks")
        from .tasks import register_image
        # ここ諦める
        # 画面キャプチャタスク
        # capture_task_record = TaskRecord()
        # task_id = capture_slide.delay().id
        # capture_task_record.task_id = task_id
        # capture_task_record.state = 0
        # 画像登録タスク
        register_image_record = TaskRecord()
        register_id = register_image.delay().id
        register_image_record.task_id = register_id
        register_image_record.state = 0
        register_image_record.type = 1
        register_image_record.save()
        return redirect("ghostwriter:tasks")


class TaskView(TemplateView):
    template_name = "ghostwriter/task_abstract.html"

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        context["tasks"] = TaskRecord.objects.all().order_by('-id')
        return context
