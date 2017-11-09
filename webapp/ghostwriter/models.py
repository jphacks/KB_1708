from django.db import models
from django.conf import settings
import os
import uuid
import enum


class BaseChoices(enum.Enum):
    @classmethod
    def choices(cls):
        return ((m.value, m.name) for m in cls)


class TaskState(BaseChoices):
    RUNNING = 0
    DONE = 1
    FAIL = 2


class TaskType(BaseChoices):
    CAPTURE = 0
    ANALYSIS = 1
    OCR = 2
    REGISTER = 3


def delete_previous_file(func):
    def wrapper(*args, **kwargs):
        self = args[0]

        # 保存前のファイル名を取得
        result = Image.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Image, self).save()

        # 関数実行
        result = func(*args, **kwargs)
        result = Image.objects.filter(pk=self.pk)
        current = result[0] if len(result) else None

        # 保存前のファイルがあったら削除
        if previous and previous != current:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, previous.image.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, previous.image.name))
        return result

    return wrapper


def get_image_path(instance, filename):
    prefix = 'images/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Lecture(models.Model):
    __days_of_week = (
        (0, '集中'),
        (1, '月曜日'),
        (2, '火曜日'),
        (3, '水曜日'),
        (4, '木曜日'),
        (5, '金曜日'),
        (6, '土曜日'),
        (7, '日曜日'),
    )
    __periods = ((p, str(p) + "限") for p in range(1, 7))
    title = models.CharField("タイトル", max_length=255)
    day_of_week = models.IntegerField("曜日", choices=__days_of_week)
    period = models.IntegerField('時限', choices=__periods)
    ocr_text = models.TextField("OCR", null=True, blank=True)
    is_parsed = models.BooleanField("Is Parsed", default=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField("タイトル", max_length=255)
    image = models.ImageField('Image', upload_to=get_image_path)
    lecture = models.ForeignKey(Lecture, related_name="images", null=True, blank=True)
    ocr = models.TextField("OCR", null=True, blank=True)
    ocr_json = models.TextField("JSON", null=True, blank=True)

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Image, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Image, self).delete()

    def __str__(self):
        return self.title


class TaskRecord(models.Model):
    type = models.IntegerField(choices=TaskType.choices())
    state = models.IntegerField(choices=TaskState.choices())
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    task_id = models.CharField("TaskID", max_length=255)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.created_at.strftime("%Y/%m/%d %H:%M:%S") + "-" + \
               self.get_type_display() + "-" + self.get_state_display()


class OCRTaskRecord(TaskRecord):
    lecture = models.ForeignKey(Lecture, related_name='task_records')
