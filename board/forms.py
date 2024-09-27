from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Announcement, Response


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        widgets = {
            'text': SummernoteWidget(),
        }
        fields = [
            'title',
            'text',
            'category'
        ]
        text = SummernoteTextField()


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]
