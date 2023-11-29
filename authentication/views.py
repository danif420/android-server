from rest_framework import permissions, views, status,viewsets
from rest_framework.response import Response
from django.contrib.auth import login
from authentication.models import Product
from authentication.serializers import ProductSerializer

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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer