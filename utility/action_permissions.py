from rest_framework.permissions import IsAuthenticated, IsAdminUser

AUTHENTICATED_ALL = {
        IsAuthenticated: ['update', 'partial_update', 'destroy', 'create', 'retrieve', 'list'],
    }

ADMIN_CREATE_UPDATE_VIEW_AUTHENTICATED = {
        IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
        IsAuthenticated: ['retrieve', 'list']
    }
