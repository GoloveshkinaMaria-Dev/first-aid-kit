from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import AvatarSerializer


class UserViewSet(DjoserUserViewSet):
    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=["put"],
        url_path="me/avatar",
        permission_classes=[permissions.IsAuthenticated],
    )
    def avatar(self, request):
        user = request.user
        serializer = AvatarSerializer(user, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        avatar_url = request.build_absolute_uri(user.avatar.url) if user.avatar else None
        return Response({"avatar": avatar_url})

    @avatar.mapping.delete
    def delete_avatar(self, request):
        user = request.user
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
