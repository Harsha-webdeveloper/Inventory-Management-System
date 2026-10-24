from rest_framework.permissions import BasePermission,SAFE_METHODS

class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True

        groups = user.groups.values_list("name",flat=True)

    #Employee : Read only
        if "Employee" in groups:
            return request.method in SAFE_METHODS
        
    # Manager :- Read,create,update
        if "Manager" in groups:
            if request.method == "DELETE":
                return False
            return True
    #admin : Full Access
        if "Admin" in groups:
            return True

        return False