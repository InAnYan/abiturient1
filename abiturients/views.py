from django.http import JsonResponse
from abiturients.models import Abiturient


def make_view(name):
    def view(request):
        q = Abiturient.objects
        if request.GET.get("q"):
            q = q.filter(**{name + "__istartswith": request.GET["q"]})

        return JsonResponse(list(q.values_list(name, flat=True).distinct()), safe=False)

    return view


birth_country = make_view("birth_country")
birth_town = make_view("birth_town")
nationality = make_view("nationality")
foreign_language = make_view("foreign_language")
