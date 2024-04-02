from django.urls import path

from abiturients.forms import AbiturientForm

from . import views, forms


urlpatterns = [
    path(
        "",
        views.AbiturientAndOffersWizard.as_view(),
        name="form",
    ),
    path("done", views.done, name="done"),
]
