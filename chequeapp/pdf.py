import base64

import requests
import json

from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from cheque_service import config, settings

host = settings.HOST_RQ


def html_to_pdf(data, check):
    content = get_complete_html(data)
    id_order = content['id_order']

    base64_contents = encode_html(content, check.type)
    filename = get_filename(id_order, check.type)
    write_pdf_in_model(base64_contents, filename, check)


def get_complete_html(data):
    content = {
        'id_order': data["id"],
        'address': data["address"],
        'phone': data['client']["phone"],
        'name': data['client']["name"],
        'items': data['items'],
        # 'price': sum([items['unit_price'] * items['quantity'] for items in data['items']]),
        'price': data['price'],
    }
    return content


def encode_html(content, type_check):
    rendered_template = render_to_string(f'chequeapp/{type_check}_check.html', content)
    contents = rendered_template.encode('utf-8')
    base64_contents = base64.b64encode(contents).decode()
    return base64_contents


def get_filename(id_order, type_check):
    return f'{id_order}_{type_check}'


def write_pdf_in_model(base64_contents, filename, check):
    data = {
        'contents': base64_contents
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(host, data=json.dumps(data), headers=headers)
    check.status = config.STATUS_RENDERED
    check.pdf_file.save(f'{filename}.pdf', ContentFile(response.content))
