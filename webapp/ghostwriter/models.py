from django.db import models
from django.conf import settings
import os
import uuid


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


class Image(models.Model):
    title = models.CharField("タイトル", max_length=255)
    image = models.ImageField('Image', upload_to=get_image_path)
    lecture = models.ForeignKey(Lecture, related_name="images", null=True, blank=True)
    ocr = models.TextField("OCR", null=True, blank=True)

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Image, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Image, self).delete()



