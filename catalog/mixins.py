from django.http import Http404
from django.contrib.auth.models import Group


class OwnerOrModeratorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # Проверка, является ли пользователь владельцем или модератором
        if obj.owner != request.user and not request.user.groups.filter(name='moderators').exists():
            raise Http404("У вас нет прав на выполнение этого действия.")

        return super().dispatch(request, *args, **kwargs)
