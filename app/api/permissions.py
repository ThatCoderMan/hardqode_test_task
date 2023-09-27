from education.models import ProductAccess
from rest_framework.permissions import BasePermission


class HasAccessPermission(BasePermission):
    message = "User do not have access to product."

    def has_permission(self, request, view):
        user = view.kwargs["user"]
        product = view.kwargs["product"]
        return ProductAccess.objects.filter(user=user, product=product).exists()
