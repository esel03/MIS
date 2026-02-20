from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.doctor import DoctorCreateUpdateSerializer
from ..services.doctor import DoctorService

service = DoctorService()


class DoctorCreateView(APIView):
    def post(self, request):
        result = service.create_doctor(data=request.data)
        return Response(data=result)