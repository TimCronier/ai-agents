from django.urls import include, path

urlpatterns = [
    path("", include("chat.urls")),        # route toutes les URLs vers l’app
    # path("admin/", include("django.contrib.admin.urls")),
]
