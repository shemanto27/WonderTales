from rest_framework.routers import DefaultRouter
from .views import StoryModelViewSet

router = DefaultRouter()
router.register(r'stories', StoryModelViewSet, basename='story')

urlpatterns = router.urls