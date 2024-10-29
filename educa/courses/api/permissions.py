from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        '''ПРоверка, присутствует ли пользователь во взаимосвязи students'''
        return obj.students.filter(id=request.user.id).exists()