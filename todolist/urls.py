from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from Todo import settings
from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'subtasks', SubTaskViewSet, basename='subtasks')

urlpatterns = [
    path('',  include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('statistics/users/', statistics_users, name='statistics-users')
]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)