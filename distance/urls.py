from django.urls import path

from distance import views

urlpatterns = [
    
path("trip/<str:origin_code_or_coords>/<str:destination_code_or_coords>/<str:mode>/", views.plan_trip, name="plan_trip"),

]
