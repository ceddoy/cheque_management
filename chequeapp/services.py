import django_rq
from django.db.models import Q

from chequeapp.constance import CHEQUE_CLIENT, CHEQUE_KITCHEN
from chequeapp.models import Printer, Check
from chequeapp.tasks import task_convert_from_html_to_pdf


def create_checks(data):

    order = data.validated_data['order']
    point = data.validated_data['order']['point_id']
    printer_kitchen = Printer.objects.filter(Q(point=point) & Q(check_type=CHEQUE_KITCHEN)).first()
    printer_client = Printer.objects.filter(Q(point=point) & Q(check_type=CHEQUE_CLIENT)).first()

    if not printer_kitchen and not printer_client:
        raise Printer.DoesNotExist

    elif printer_kitchen and printer_client:
        checks = Check.objects.bulk_create(
            [
                Check(type=CHEQUE_KITCHEN, printer=printer_kitchen, order=order),
                Check(type=CHEQUE_CLIENT, printer=printer_client, order=order)
            ]
        )
        for check in checks:
            django_rq.enqueue(task_convert_from_html_to_pdf, data=order, check=check)

    else:
        if printer_kitchen:
            check = Check.objects.create(type=CHEQUE_KITCHEN, printer=printer_kitchen, order=order)
        else:
            check = Check.objects.create(type=CHEQUE_CLIENT, printer=printer_client, order=order)

        django_rq.enqueue(task_convert_from_html_to_pdf, data=order, check=check)


def check_identical_cheques(id_check):
    for check in Check.objects.all():
        if check.order["id"] == id_check:
            return True
    return False
