from django.urls import path
from zixishi import views

urlpatterns = [
    path('', views.Prepare.as_view()),
    path('download', views.down),
]
