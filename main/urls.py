from django.urls import path
from .api.doctor import DoctorCreateView

urlpatterns = [
    path("doctor/", DoctorCreateView.as_view(), name="doctor-create"),
]