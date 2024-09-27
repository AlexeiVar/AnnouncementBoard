from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AnnouncementList.as_view(), name='announcement_list'),
    path('<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('create', AnnouncementCreate.as_view(), name='announcement_create'),
]
