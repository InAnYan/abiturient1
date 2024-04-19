from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="pk_panel"),
    path("gen_doc", views.gen_doc, name="gen_doc"),
]
