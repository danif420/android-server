from rest_framework import permissions, views, status,viewsets,generics
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from authentication.models import Product
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.serializers import ProductSerializer,ProductCreateSerializer,UserSerializer
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

class LogoutView(views.APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        del request.session['username':username]
        del request.session['password':password]
        del request.delete_cookie['username': username]
        del request.delete_cookie['password':password]
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

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

    def create(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        return Product.objects.filter(name__icontains=query)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class BuyProductAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.quantity > 0:
            instance.quantity -= 1
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({"detail": "Product out of stock."}, status=400)

def get_3d_model(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    model_path = product.model_3d.path
    model_uri = request.build_absolute_uri(model_path)
    return JsonResponse({'modeluri': model_uri})