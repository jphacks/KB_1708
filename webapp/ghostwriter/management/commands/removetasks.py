from __future__ import absolute_import
from django.core.management.base import BaseCommand
from ghostwriter.models import TaskRecord, OCRTaskRecord


class Command(BaseCommand):
    help = "Remove image from specified lecture"

    def handle(self, *args, **options):
        tasks = TaskRecord.objects.all()
        ocr_tasks = OCRTaskRecord.objects.all()
        for task in tasks:
            task.delete()
        for ocr_task in ocr_tasks:
            ocr_task.delete()
