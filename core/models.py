from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Manga(models.Model):
    series_name = models.CharField(max_length=255)
    manga_reader_url = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return self.series_name


class Kindle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kindle_model = models.CharField(max_length=100, blank=True)
    kindle_email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)


class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapter = models.CharField(max_length=255)
    # TODO add new field to list chapter number, grabbing # from chapter string using regex, for better sort (natsort)
    chapter_title = models.CharField(max_length=255)
    chapter_url = models.CharField(max_length=255)
    chapter_date = models.DateField()


class ChapterScan(models.Model):
    manga = models.OneToOneField(Manga, on_delete=models.CASCADE, primary_key=True)
    triggered_by = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    last_scanned_at = models.DateField(default=timezone.now)


class SystemLog(models.Model):
    operation = models.CharField(max_length=255)
    triggered_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)

    def save_log(self, operation, trigger_user):
        self.operation = operation
        self.triggered_by = trigger_user
        self.save()


class MailingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    manga = models.ForeignKey(Manga, on_delete=models.DO_NOTHING)
    chapter_sent = models.IntegerField()
    sent_date = models.DateTimeField(default=timezone.now)

    def save_log(self, user_id, manga_id, chapter_num):
        self.user = user_id
        self.manga_id = manga_id
        self.chapter_sent = chapter_num
        self.save()
