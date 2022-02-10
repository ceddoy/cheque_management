CHEQUE_KITCHEN = 'kitchen'
CHEQUE_CLIENT = 'client'

CHEQUE_CHOICES = (
    (CHEQUE_KITCHEN, 'Кухня'),
    (CHEQUE_CLIENT, 'Клиент'),
)


STATUS_NEW = 'new'
STATUS_RENDERED = 'rendered'
STATUS_PRINTED = 'printed'

CHOICES_STATUS_CHEQUE = (
    (STATUS_NEW, 'Новый'),
    (STATUS_RENDERED, 'Полученный'),
    (STATUS_PRINTED, 'Напечатанный'),
)