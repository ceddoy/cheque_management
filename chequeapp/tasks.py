from cheque_service import config
from chequeapp import pdf


def task_convert_from_html_to_pdf(data, check):
    pdf.html_to_pdf(data, check)


def task_change_status_check(obj):
    obj.status = config.STATUS_PRINTED
    obj.save(update_fields=['status'])
