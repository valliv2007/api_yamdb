from rest_framework import mixins, viewsets


class GetPostDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Вьюсет для просмотра всех экземпляров, публикации и удаления"""


class GetUpdate(mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """Вьюсет для просмотра всех экземпляров и обновления"""
