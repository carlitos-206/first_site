from finalAPP.models import Trip
from django.urls import path
from . import views
urlpatterns = [
    # login/registration urls
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    # trip urls
    path("addTripForm", views.tripform),
    path('addTrip', views.add),
    path("delete/<int:trip_id>", views.destroyTrip),
    path('<int:trip_id>/edit', views.editTrip),
    path('<int:trip_id>/update', views.update),
    path('<int:trip_id>', views.tripInfo)
]
