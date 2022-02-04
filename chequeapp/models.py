from django.db import models
from django.utils.crypto import get_random_string
from rest_framework_api_key.models import APIKey

from cheque_service.config import CHEQUE_CHOICES, CHOICES_STATUS_CHEQUE, STATUS_NEW


class Printer(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название принтера')
    api_key = models.CharField(max_length=100, unique=True, blank=True, verbose_name='API ключ')
    check_type = models.CharField(max_length=64, choices=CHEQUE_CHOICES, verbose_name='Тип чека')
    point = models.PositiveIntegerField(verbose_name='Магазин')

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.api_key:
            self.api_key = self.__get_api_key()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @staticmethod
    def __get_api_key():
        return get_random_string(length=32)

    def __str__(self):
        return self.name


class Check(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.PROTECT, verbose_name='Принтер')
    type = models.CharField(max_length=64, choices=CHEQUE_CHOICES, verbose_name='Тип чека')
    order = models.JSONField(verbose_name='Информация о заказе')
    status = models.CharField(max_length=64, choices=CHOICES_STATUS_CHEQUE, default=STATUS_NEW, verbose_name='Статус чека')
    pdf_file = models.FileField(upload_to='pdf', blank=True, max_length=254)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f'{self.order["id"]}'

