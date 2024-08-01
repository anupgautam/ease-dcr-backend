from rest_framework import viewsets
from .models import ContactUs
from .serializers import ContactUsSerializer
from rest_framework.response import Response

class ContactUsViewset(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)