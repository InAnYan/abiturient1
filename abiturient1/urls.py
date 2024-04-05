"""
URL configuration for abiturient1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from abiturient1.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

"""
admin.site.index_title = _("admin.site.index_title")
admin.site.site_header = _("admin.site.site_header")
admin.site.site_title = _("admin.site.site_title")
"""

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls, name="admin"),
    path("", include("accepting_offers.urls")),
) + [
    path("univeristy_offers/", include("university_offers.urls")),
]

if DEBUG:
    urlpatterns += [
        path("__debug__", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
