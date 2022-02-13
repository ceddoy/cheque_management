from django.urls import path, include
from django.views.decorators.cache import cache_page

from chequeapp import views as chequeapp

app_name = 'chequeapp'

urlpatterns = [
    path('create_checks/', chequeapp.CreateCheckAPIView.as_view()),
    path('new_checks/', cache_page(60 * 15)(chequeapp.NewChecksListAPIView.as_view())),
    path('check/', chequeapp.CheckAPIView.as_view()),
]
