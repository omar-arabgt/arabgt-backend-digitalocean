from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsOwnerOrReadOnlyPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
