from rest_framework import viewsets, filters, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from collaboration.models import TripCollaborator, TripInvitation
from .serializers import (
    CollaboratorSerializer,
    InvitationSerializer,
    InvitationResponseSerializer
)

class CollaboratorViewSet(viewsets.ModelViewSet):
    """ViewSet for TripCollaborator CRUD operations"""
    serializer_class = CollaboratorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['trip', 'role']
    ordering = ['-added_at']

    def get_queryset(self):
        """Return collaborators for trips owned by or shared with current user"""
        user = self.request.user
        return TripCollaborator.objects.filter(
            Q(trip__user=user) | Q(user=user)
        )

    def perform_create(self, serializer):
        """Prevent duplicate collaborators"""
        trip = serializer.validated_data['trip']
        user = serializer.validated_data['user']

        if TripCollaborator.objects.filter(trip=trip, user=user).exists():
            raise serializers.ValidationError(
                "User is already a collaborator on this trip"
            )

        serializer.save()


class InvitationViewSet(viewsets.ModelViewSet):
    """ViewSet for TripInvitation CRUD operations"""
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['trip', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return invitations sent by or received by current user"""
        user = self.request.user
        return TripInvitation.objects.filter(
            Q(inviter=user) | Q(invitee_email=user.email)
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Accept or decline invitation"""
        invitation = self.get_object()
        serializer = InvitationResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action_type = serializer.validated_data['action']

        # Check if invitation is for current user
        if invitation.invitee_email != request.user.email:
            return Response(
                {'error': 'This invitation is not for you'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if expired
        if invitation.is_expired:
            invitation.status = 'expired'
            invitation.save()
            return Response(
                {'error': 'Invitation has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action_type == 'accept':
            invitation.status = 'accepted'
            invitation.save()

            # Create collaborator
            TripCollaborator.objects.create(
                trip=invitation.trip,
                user=request.user,
                role=invitation.role
            )

            return Response({'message': 'Invitation accepted successfully'})

        elif action_type == 'decline':
            invitation.status = 'declined'
            invitation.save()
            return Response({'message': 'Invitation declined'})
