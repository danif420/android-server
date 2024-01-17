from django.contrib import admin
from django.urls import path, include
from authentication import views
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token),
    path('logout/', views.LogoutView.as_view()),
    path('signup/', views.UserCreateView.as_view()),
    path('get_user_id/<str:username>/', views.GetUserIdView.as_view()),
    path('get_user/<int:id>/', views.get_user),
    path('delete_user/<int:pk>/', views.UserDeleteView.as_view()),
    path('api/', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)