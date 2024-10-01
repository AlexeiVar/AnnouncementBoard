from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from django.shortcuts import render, redirect
from .forms import *
from .filters import *
from .tasks import announcement_created_notification, response_created_notification

# Create your views here.

class AnnouncementList(ListView):
    paginate_by = 5
    model = Announcement
    ordering = '-date'
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcement_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnnouncementFitler(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


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
        announcement_created_notification.delay(announcement.pk)
        return super().form_valid(form)


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'announcements/response_create.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.sender = self.request.user
        response.announcement = Announcement.objects.get(id=self.kwargs['pk'])
        response.receiver = (Announcement.objects.get(id=self.kwargs['pk'])).creator
        response.save()
        response_created_notification.delay(response.pk)
        return super().form_valid(form)


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'announcements/response_delete.html'
    success_url = reverse_lazy('responses')


class ResponseList(LoginRequiredMixin, ListView):
    paginate_by = 15
    model = Response
    ordering = ('-acceptance', '-date')
    template_name = 'announcements/responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(receiver=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Сделано как view ибо это позволяет проверить, что принимающий имеет право это делать
# в то время как если сделать как с подписками (ниже в файле), то все у кого будет ссылка смогут это сделать
class ResponseAcceptance(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'announcements/response_accept.html'


class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_delete.html'
    success_url = reverse_lazy('announcement_list')


class AnnouncementEdit(LoginRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcements/announcement_edit.html'


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'announcements/category_list.html'
    context_object_name = 'category_list'


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)
