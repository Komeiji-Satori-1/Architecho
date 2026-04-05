from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CoCreationItem
from .serializers import CoCreationNewsSerializer, CoCreationListSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_news(request):
    """
    首页「共创动态」：返回最近采纳的 2 条共创。
    GET /api/cocreation/recent-news/
    返回：[{id, type, label, content}, ...]
    """
    items = (
        CoCreationItem.objects
        .filter(status=CoCreationItem.STATUS_ADOPTED)
        .select_related('author')
        .order_by('-updated_at')[:2]
    )
    serializer = CoCreationNewsSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)


class CoCreationItemViewSet(viewsets.ModelViewSet):
    queryset = CoCreationItem.objects.select_related('author').all()
    serializer_class = CoCreationListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            qs = qs.filter(featured=True)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
