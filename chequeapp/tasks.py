from chequeapp import pdf
from chequeapp.constance import STATUS_PRINTED


def task_convert_from_html_to_pdf(data, check):
    pdf.html_to_pdf(data, check)


def task_change_status_check(obj):
    obj.status = STATUS_PRINTED
    obj.save(update_fields=['status'])
