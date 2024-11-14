from django.http import Http404
from django.contrib.auth.models import Group


class ContentManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # Проверка, является ли пользователь владельцем или модератором
        if not request.user.groups.filter(name='content_manager').exists():
            raise Http404("У вас нет прав на выполнение этого действия.")

        return super().dispatch(request, *args, **kwargs)
