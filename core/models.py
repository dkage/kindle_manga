from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Kindle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kindle_model = models.CharField(max_length=100, blank=True)
    kindle_email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)


class Manga(models.Model):
    series_name = models.CharField(max_length=255)
    manga_reader_url = models.CharField(max_length=255)


class ChapterInfo(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    num_chapters = models.IntegerField()
    last_chapter = models.CharField(max_length=255)
    last_scan_date = models.DateField()


class SystemLog(models.Model):
    operation = models.CharField(max_length=255)
    triggered_by = models.CharField(max_length=255)
    date = models.DateTimeField()


class SendLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    manga = models.ForeignKey(Manga, on_delete=models.DO_NOTHING)
    chapter_sent = models.IntegerField()
    sent_date = models.DateField()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)