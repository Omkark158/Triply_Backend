from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, ActivityViewSet

router = DefaultRouter()
router.register('destinations', DestinationViewSet, basename='destination')
router.register('activities', ActivityViewSet, basename='activity')

urlpatterns = router.urls