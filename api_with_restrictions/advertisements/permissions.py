from rest_framework.permissions import BasePermission, SAFE_METHODS

#Ограничение на удаление и изменение, у админов полные права
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS or request.user.is_staff:
            return True
        return obj.creator == request.user


#Ограничение на просмотр Черновиков только для создателей, у админов прав на просмотр нет
class IsDraftStatus(BasePermission):
    def has_object_permission(self, request, view, obj):

        if obj.status == 'DRAFT':
            return obj.creator == request.user