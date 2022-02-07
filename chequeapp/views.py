import django_rq
from django.http import JsonResponse, FileResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView

from chequeapp import services
from chequeapp.filters import ChecksFilter, CheckFilter
from chequeapp.models import Check, Printer
from chequeapp.serializer import CreateCheckSerializer, NewChecksSerializer
from chequeapp.tasks import task_change_status_check


class CreateCheckAPIView(CreateAPIView):
    """Создание чеков"""
    queryset = Check.objects.all()
    serializer_class = CreateCheckSerializer

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
            return JsonResponse({"ok": "Чеки успешно созданы"})
        except Printer.DoesNotExist:
            return JsonResponse({"error": "Для данной точки не настроено ни одного принтера"},
                                status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        services.create_checks(serializer)


class NewChecksListAPIView(ListAPIView):
    """Список чеков, которые еще не распечатаны"""
    serializer_class = NewChecksSerializer
    filterset_class = ChecksFilter
    queryset = Check.objects.all()

    def list(self, request, *args, **kwargs):
        error = Printer.check_api_key(request.query_params.get('api_key'))
        if error:
            return error
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"checks": list(serializer.data)})


class CheckAPIView(GenericAPIView):
    """Вывод чека на печать"""
    queryset = Check.objects.all()
    filterset_class = CheckFilter

    def get(self, request, *args, **kwargs):
        error = Printer.check_api_key(request.query_params.get('api_key'))
        if error:
            return error
        obj = self.filter_queryset(self.get_queryset())
        if obj is None:
            return JsonResponse({"error": "Данного чека не существует"},
                                status=status.HTTP_400_BAD_REQUEST)
        if not obj.pdf_file:
            return JsonResponse({"error": "Для данного чека не сгенерирован PDF-файл"},
                                status=status.HTTP_400_BAD_REQUEST)
        django_rq.enqueue(task_change_status_check, obj)
        return FileResponse(obj.pdf_file.file)

