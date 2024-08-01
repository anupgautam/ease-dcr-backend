from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'country', CountryViewset)
router.register(r'city', CityViewset)

urlpatterns = router.urls
