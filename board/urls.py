from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AnnouncementList.as_view(), name='announcement_list'),
    path('create', AnnouncementCreate.as_view(), name='announcement_create'),

    path('<int:pk>/', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('<int:pk>/edit', AnnouncementEdit.as_view(), name='announcement_edit'),
    path('<int:pk>/respond', ResponseCreate.as_view(), name='respond'),

    path('responses/', ResponseList.as_view(), name='responses'),
    path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='delete_response'),
    path('responses/<int:pk>/accept', ResponseAcceptance.as_view(), name='accept_response'),

    path('category', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]
