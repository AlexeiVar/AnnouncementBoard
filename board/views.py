from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.

class AnnouncementList(ListView):
    paginate_by = 3
    model = Announcement
    ordering = '-date'
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcement_list'


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement_detail'


class AnnouncementCreate(LoginRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcements/announcement_create.html'

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.creator = self.request.user
        announcement.save()
        return super().form_valid(form)
