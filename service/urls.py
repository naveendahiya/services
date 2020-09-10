from django.urls import path, include
# from rest_framework.urlpatterns import format_suffix_patterns
from service import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'bids', views.BidViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login')
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
