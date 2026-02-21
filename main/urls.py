from django.urls import path
from .api.doctor import DoctorCreateView, DoctorUpdateView

urlpatterns = [
    path("doctor/create", DoctorCreateView.as_view(), name="doctor-create"),
    path("doctor/update", DoctorUpdateView.as_view(), name="doctor-update"),
]