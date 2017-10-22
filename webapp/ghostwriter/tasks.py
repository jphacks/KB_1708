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


@task
def register_image():
    # register image
    import os
    from django.core.files import File
    from datetime import datetime
    from .models import Image
    files = check_file("media/cache", ".jpg")
    now = datetime.now()
    for i, file in enumerate(files):
        with open("media/cache/" + file, "rb") as jpg:
            django_file = File(jpg)
            img = Image()
            img.image.save(now.strftime("%Y-%m-%d %H:%M:%S") + "-" + str(i) + ".jpg", django_file, save=True)
            img.title = now.strftime("%Y-%m-%d %H:%M:%S") + "-" + str(i)
            img.save()
        os.remove("media/cache/" + file)


def on_task_revoked(*args, **kwargs):
    print(str(kwargs))
    print('task_revoked')


task_revoked.connect(on_task_revoked, dispatch_uid='on_task_revoked')
