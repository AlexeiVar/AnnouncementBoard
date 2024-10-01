from django_filters import FilterSet, DateFilter
from .models import Response, Announcement
from django import forms


class ResponseFilter(FilterSet):
    class Meta:
        model = Response

        fields = ('announcement', 'acceptance')


class AnnouncementFitler(FilterSet):
    date = DateFilter(
        field_name='date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__lte',
    )

    class Meta:
        model = Announcement

        fields = ('category',)
