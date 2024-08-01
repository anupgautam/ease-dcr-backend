from rest_framework.routers import DefaultRouter
from .views import ContactUsViewset


router = DefaultRouter()

router.register(r'contact-us', ContactUsViewset)

urlpatterns = router.urls
