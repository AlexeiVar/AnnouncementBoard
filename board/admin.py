from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class AnnouncementAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)


# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Response)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Categories)
