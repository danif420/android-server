from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    path('api/', include('authentication.urls')),
]