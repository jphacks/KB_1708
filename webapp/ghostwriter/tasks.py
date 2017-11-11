from celery.task import task
from celery.signals import task_revoked

# 諦める
# @task
# def capture_slide():
#     print("task called")
#     import os
#     from django.conf import settings
#     from .capture_lib import SlideCapture, SlideCaptureError
#     try:
#         with SlideCapture(1) as cap:
#             cap.monitor_slides(os.path.join(settings.BASE_DIR, "media", "cache"))
#     except SlideCaptureError:
#         pass


def check_file(path='./', ext=''):
    import os
    _ch = os.listdir(path)
    ch_e = []
    for _ in _ch:
        _root, _ext = os.path.splitext(_)
        if _ext == ext and _root != "calibration":
            ch_e.append(_)
    return ch_e


@task(bind=True)
def register_image(self):
    # register image
    import os
    from django.core.files import File
    from django.conf import settings
    from datetime import datetime
    from .models import Image, TaskState, TaskType, TaskRecord
    record = TaskRecord(
        task_id=self.request.id,
        state=TaskState.RUNNING.value,
        type=TaskType.REGISTER.value
    )
    record.save()
    cache_dir = os.path.join(settings.MEDIA_ROOT, 'cache')
    files = check_file(cache_dir, ".jpg")
    now = datetime.now()
    try:
        for i, file in enumerate(files):
            image_path = os.path.join(cache_dir, file)
            with open(image_path, "rb") as jpg:
                django_file = File(jpg)
                img = Image()
                img.image.save(now.strftime("%Y-%m-%d %H:%M:%S") + "-" + str(i) + ".jpg", django_file, save=True)
                img.title = now.strftime("%Y-%m-%d %H:%M:%S") + "-" + str(i)
                img.save()
            os.remove(image_path)
        record.state = TaskState.DONE.value
    except Exception:
        record.state = TaskState.FAIL.value
    finally:
        record.save()


@task(bind=True)
def get_ocr_text(self, lecture_id: int, new_image_id: list):
    from logging import getLogger
    from django.conf import settings
    from .models import Lecture, Image, TaskState, TaskType, OCRTaskRecord
    from .capture_lib import GoogleOCR
    lecture = Lecture.objects.get(id=lecture_id)
    record = OCRTaskRecord.objects.create(
        task_id=self.request.id,
        state=TaskState.RUNNING.value,
        type=TaskType.OCR.value,
        lecture=lecture
    )
    ocr = GoogleOCR(api_key=settings.GCV_API_KEY)
    new_images = list()
    for i in new_image_id:
        image = Image.objects.get(id=i)
        image.lecture = lecture
        image.save()
        new_images.append(image)
    paths = [i.image.path for i in new_images]
    try:
        results = ocr.get_jsons(paths)
        for res, image in zip(results, new_images):
            text = ocr.parse_description(res)
            image.ocr = text
            image.ocr_json = res
            image.save()
        ocr_text = ""
        for i in lecture.images.all():
            ocr_text += i.ocr
        lecture.ocr_text = ocr_text
        record.state = TaskState.DONE.value
    except Exception as e:
        logger = getLogger('OCRTask')
        logger.exception(e.args)
        for i in new_image_id:
            lecture.images.remove(i)
        lecture.is_parsed = True
        record.state = TaskState.FAIL.value
    finally:
        record.save()
        lecture.save()


@task
def empty_task():
    from time import sleep
    sleep(10)


def on_task_revoked(*args, **kwargs):
    print(str(kwargs))
    print('task_revoked')


task_revoked.connect(on_task_revoked, dispatch_uid='on_task_revoked')
