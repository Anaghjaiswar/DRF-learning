from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Custom permission to allow only the owner of a recipe to edit or delete it.

    def has_object_permission(self,request,view,obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the recipe
        return obj.created_by == request.user
    
    