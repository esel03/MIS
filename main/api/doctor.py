from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.doctor import DoctorService

service = DoctorService()


class DoctorCreateView(APIView):
    def post(self, request):
        result = service.create_doctor(data=request.data)
        return Response(data=result)


class DoctorUpdateView(APIView):
    def patch(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token or not token.startswith('Bearer '):
            return Response(
                {"error": "Требуется токен Bearer"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        token = token.split(' ')[1]
        result = service.update_doctor(pk=int(token), data=request.data)
        return Response(data=result)