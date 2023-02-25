from rest_framework.permissions import BasePermission

class ValidateKey(BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key == 'valid_key':
            return True
        return False
