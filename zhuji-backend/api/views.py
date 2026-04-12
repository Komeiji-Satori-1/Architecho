from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.http import HttpResponse

from forum.models import ForumPost
from forum.serializers import ForumPostListSerializer
from monuments.models import Monument
from monuments.serializers import MonumentSerializer
from cocreation.models import CoCreationItem
from cocreation.serializers import CoCreationListSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def global_search(request):
    q = request.query_params.get('q', '').strip()
    if not q:
        return Response({'posts': [], 'monuments': [], 'cocreations': []})

    posts = ForumPost.objects.filter(
        Q(title__icontains=q) | Q(excerpt__icontains=q)
    ).select_related('author', 'category')[:20]

    monuments = Monument.objects.filter(
        Q(name__icontains=q) | Q(location__icontains=q) | Q(dynasty__icontains=q) | Q(desc__icontains=q),
        is_published=True,
    )[:20]

    cocreations = CoCreationItem.objects.filter(
        Q(title__icontains=q) | Q(desc__icontains=q) | Q(material__icontains=q)
    ).select_related('author')[:20]

    return Response({
        'posts': ForumPostListSerializer(posts, many=True, context={'request': request}).data,
        'monuments': MonumentSerializer(monuments, many=True, context={'request': request}).data,
        'cocreations': CoCreationListSerializer(cocreations, many=True, context={'request': request}).data,
    })
def admin_honeypot(request):
    # 记录 IP（这里可以结合你的日志系统）
    ip = request.META.get('REMOTE_ADDR')
    # 返回一个伪装成系统崩溃的 401 或 404
    return HttpResponse("Internal Server Error: Debug mode disabled.", status=401)