from django.urls import path
from .views import PredictVoucherView

urlpatterns = [
    path('predict/', PredictVoucherView.as_view(), name='predict-voucher'),
]
