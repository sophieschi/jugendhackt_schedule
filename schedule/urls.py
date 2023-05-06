from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>.xml", views.schedule_xml, name="schedule_xml"),
]
