from django.db.models import Q
from django.http import JsonResponse, FileResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView

from cheque_service import config
from chequeapp import services
from chequeapp.models import Check, Printer
from chequeapp.serializer import CreateCheckSerializer, NewChecksSerializer, CheckSerializer


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

    def get_queryset(self):
        return Check.objects.filter(Q(printer=Printer.objects.get(api_key=self.request.data.get('api_key'))) &
                                    Q(status=config.STATUS_RENDERED)).select_related('printer').values('id')

    def list(self, request, *args, **kwargs):
        try:
            data = super().list(request, *args, **kwargs)
            return JsonResponse({"checks": list(data.data)})
        except Printer.DoesNotExist:
            return JsonResponse({"error": "Ошибка авторизации"},
                                status=status.HTTP_401_UNAUTHORIZED)


class CheckAPIView(APIView):
    """Вывод чека на печать"""
    def get(self, request, *args, **kwargs):
        return self.process_cheque_for_printing(request.data)

    def get_object(self, data):
        return Check.objects.filter(Q(printer=Printer.objects.get(api_key=data.get('api_key'))) &
                                    Q(id=data.get('check_id'))).first()

    def check_cheque_for_errors(self, data):
        try:
            obj = self.get_object(data)
        except Printer.DoesNotExist:
            return JsonResponse({"error": "Ошибка авторизации"},
                                status=status.HTTP_401_UNAUTHORIZED)
        if obj is None:
            return JsonResponse({"error": "Данного чека не существует"},
                                status=status.HTTP_400_BAD_REQUEST)
        if not obj.pdf_file:
            return JsonResponse({"error": "Для данного чека не сгенерирован PDF-файл"},
                                status=status.HTTP_400_BAD_REQUEST)
        return obj

    def process_cheque_for_printing(self, data):
        serializer = CheckSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = self.check_cheque_for_errors(serializer.validated_data)
        self.change_status(obj)
        return FileResponse(obj.pdf_file.file)

    def change_status(self, obj):
        obj.status = config.STATUS_PRINTED
        obj.save(update_fields=['status'])
