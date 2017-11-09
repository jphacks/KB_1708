from django.contrib import admin
from .models import Image, Lecture, TaskRecord, OCRTaskRecord

# Register your models here.

admin.site.register(Image)
admin.site.register(Lecture)
admin.site.register(TaskRecord)
admin.site.register(OCRTaskRecord)
