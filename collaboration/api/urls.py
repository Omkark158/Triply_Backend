from rest_framework.routers import DefaultRouter
from .views import CollaboratorViewSet, InvitationViewSet

router = DefaultRouter()
router.register('collaborators', CollaboratorViewSet, basename='collaborator')
router.register('invitations', InvitationViewSet, basename='invitation')

urlpatterns = router.urls