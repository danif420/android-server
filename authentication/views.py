from rest_framework import permissions, views, status,viewsets,generics
from rest_framework.response import Response
from django.contrib.auth import login
from authentication.models import Product
from authentication.serializers import ProductSerializer
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from . import serializers

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"str": "success"}, status=status.HTTP_202_ACCEPTED)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def list(self, request, *args, **kwargs):
        # Call the original list method to get the serialized data
        response_data = super().list(request, *args, **kwargs)

        # Wrap the serialized data in a dictionary with a key ('products' in this case)
        response_data = {'products': response_data.data}

        return JsonResponse(response_data)

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        return Product.objects.filter(name__icontains=query)

def get_3d_model(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Assuming the 3D models are stored in the 'models' directory within MEDIA_ROOT
    model_path = product.model_3d.path

    model_uri = request.build_absolute_uri(model_path)

    return JsonResponse({'modeluri': model_uri})