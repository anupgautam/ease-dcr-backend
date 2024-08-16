from django.urls import path
from .views import DateConversionAPIView

urlpatterns = [
    path('api/convert-date/', DateConversionAPIView.as_view(), name='convert_date_api'),
]