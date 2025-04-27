from django.contrib import admin
from django.urls import path
from rental import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("bicycles/", views.bicycle_list, name="bicycle_list"),
    path("rent/<int:bicycle_id>/", views.rent_bicycle, name="rent_bicycle"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("return/<int:rental_id>/", views.return_bicycle, name="return_bicycle"),
    path("feedback/<int:rental_id>/", views.submit_feedback, name="submit_feedback"),
    path(
        "payment/<int:bicycle_id>/<int:duration>/",
        views.payment_confirm,
        name="payment_confirm",
    ),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
