from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="pk_panel"),
    path("generate-document", views.gen_doc, name="gen_doc"),
    path("generate-all-documents", views.gen_all_docs, name="gen_all_docs"),
]
