from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import ProfileWorld
from worlds.models import World, Image
from worlds.serializers import WorldSerializer, ImageSerializer


class WorldListAPIView(ListAPIView):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(WorldListAPIView, self).get_queryset()
        status = self.request.query_params.get("status", None)
        if status:
            your_worlds = ProfileWorld.objects.values_list("world__id", flat=True).filter(
                profile__user=self.request.user,
                lost=False
            ).distinct("world")
            if status == "finished":
                queryset = queryset.filter(id__in=your_worlds)
            elif status == "pending":
                queryset = queryset.exclude(id__in=your_worlds)
        return queryset


class ImageListAPIView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["world"]
    search_fields = ["id", "title"]
