"""
URL configuration for bicycle_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from rental import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.bicycle_list, name="bicycle_list"),
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
    ),  # New route
]

# from django.contrib import admin
# from django.urls import path
# from rental import views

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", views.bicycle_list, name="bicycle_list"),  # Homepage lists bicycles
#     path("rent/<int:bicycle_id>/", views.rent_bicycle, name="rent_bicycle"),
# ]


# from django.contrib import admin
# from django.urls import path
# from rental import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('rent/', views.rent_bicycle),
# ]
