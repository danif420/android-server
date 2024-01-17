from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, get_3d_model, ProductDetailAPIView, BuyProductAPIView, UserCreateView, ProductByUserIdViewSet, ProductDeleteView, ProductEditView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'user_products', ProductByUserIdViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('get_3d_model/<int:product_id>/', get_3d_model, name='get_3d_model'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product-edit'),
    path('buy/<int:id>/', BuyProductAPIView.as_view(), name='buy-product'),
]