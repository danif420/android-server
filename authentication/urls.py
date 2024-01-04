from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, get_3d_model

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('get_3d_model/<int:product_id>/', get_3d_model, name='get_3d_model')
]