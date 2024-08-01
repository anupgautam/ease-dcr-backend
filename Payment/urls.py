from rest_framework.routers import DefaultRouter
from Payment.views import *


router = DefaultRouter()
router.register(r'banks', BankViewset)
router.register(r'company-wise-bank', CompanyWiseBankViewset)
router.register(r'payment', PaymentViewset)
router.register(r'stockist-payment', StockistPaymentViewset)
urlpatterns = router.urls