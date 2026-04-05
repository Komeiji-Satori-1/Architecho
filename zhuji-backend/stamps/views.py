from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserStamp
from .serializers import StampProgressSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_progress(request):
    """
    返回当前用户进度最深的一枚印章状态，用于首页 StampLayer 组件。
    GET /api/stamps/my-progress/
    → { title, progress, collected, total, description }
    未收集任何印章时返回 404。
    """
    user_stamp = (
        UserStamp.objects
        .filter(user=request.user)
        .select_related('stamp')
        .order_by('-unlocked_layers', '-collected_at')
        .first()
    )
    if not user_stamp:
        return Response({'detail': '尚未开始收集印章。'}, status=404)
    return Response(StampProgressSerializer(user_stamp).data)
