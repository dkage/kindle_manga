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
    last_scan_date = models.DateTimeField(default=timezone.now)

    def update_chapter(self, num_chapters, last_chapter, last_scan_date):
        self.num_chapters = num_chapters
        self.last_chapter = last_chapter
        self.last_scan_date = last_scan_date
        self.save()


class SystemLog(models.Model):
    operation = models.CharField(max_length=255)
    triggered_by_id = models.CharField(max_length=255)
    triggered_by = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def save_log(self, operation, trigger_user):
        self.operation = operation
        self.triggered_by = trigger_user
        self.save()


class SendLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    manga = models.ForeignKey(Manga, on_delete=models.DO_NOTHING)
    chapter_sent = models.IntegerField()
    sent_date = models.DateTimeField(default=timezone.now)

    def save_log(self, user_id, manga_id, chapter_num):
        self.user = user_id
        self.manga_id = manga_id
        self.chapter_sent = chapter_num
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)

    def subscribe(self, user_id, manga_id):
        self.user = user_id
        self.manga = manga_id
        self.save()
