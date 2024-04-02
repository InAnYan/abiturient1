from django.urls import path

from . import views


urlpatterns = [
    path("", views.CreateAbiturientView.as_view(), name="form"),
    path("done", views.done, name="done"),
]
