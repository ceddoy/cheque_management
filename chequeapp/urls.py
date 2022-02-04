from django.urls import path

from chequeapp import views as chequeapp

app_name = 'chequeapp'

urlpatterns = [
    path('create_checks/', chequeapp.CreateCheckAPIView.as_view()),
    path('new_checks/', chequeapp.NewChecksListAPIView.as_view()),
    path('check/', chequeapp.CheckAPIView.as_view()),
]
