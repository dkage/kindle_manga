from django.contrib import admin
from core.models import *


# Register your models here.
admin.site.register(Kindle)
admin.site.register(Manga)
admin.site.register(ChapterScan)
admin.site.register(SystemLog)
admin.site.register(MailingLog)
