from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from chequeapp.constance import STATUS_RENDERED
from chequeapp.models import Check


class ChecksFilter(FilterSet):
    api_key = filters.CharFilter(method='filter_checks_by_api_key')

    class Meta:
        model = Check
        fields = ['api_key']

    def filter_checks_by_api_key(self, queryset, name, key):
        return queryset.filter(Q(printer__api_key=key) &
                               Q(status=STATUS_RENDERED)).select_related('printer').values('id')


class CheckFilter(FilterSet):
    api_key = filters.CharFilter()
    check_id = filters.CharFilter()

    class Meta:
        model = Check
        fields = ['api_key', 'check_id']

    def filter_queryset(self, queryset):
        obj = queryset.filter(Q(printer__api_key=self.form.cleaned_data.get('api_key')) &
                              Q(id=self.form.cleaned_data.get('check_id'))).first()
        return obj
