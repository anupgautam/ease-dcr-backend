# my_app/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bsdate.convertor import BSDateConverter
from .serializers import DateConversionSerializer

class DateConversionAPIView(APIView):
    def post(self, request):
        serializer = DateConversionSerializer(data=request.data)
        if serializer.is_valid():
            ad_date = serializer.validated_data.get('ad_date')
            bs_date = serializer.validated_data.get('bs_date')

            converter = BSDateConverter()
            if ad_date:
                bs_date = converter.convert_ad_to_bs(ad_date.strftime('%Y-%m-%d'))
                return Response({'ad_date': ad_date, 'bs_date': bs_date}, status=status.HTTP_200_OK)
            elif bs_date:
                ad_date = converter.convert_bs_to_ad(bs_date.strftime('%Y-%m-%d'))
                return Response({'bs_date': bs_date, 'ad_date': ad_date}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Either ad_date or bs_date is required.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
