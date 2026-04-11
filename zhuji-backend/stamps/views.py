from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Stamp, StampColorLayer, UserStamp
from .serializers import (
    StampSerializer,
    StampWriteSerializer,
    StampColorLayerSerializer,
    StampProgressSerializer,
)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_progress(request):
    user_stamp = (
        UserStamp.objects
        .filter(user=request.user)
        .select_related('stamp')
        .prefetch_related('stamp__color_layers')
        .order_by('-unlocked_layers', '-collected_at')
        .first()
    )
    if not user_stamp:
        return Response({'detail': '尚未开始收集印章。'}, status=404)
    return Response(StampProgressSerializer(user_stamp, context={'request': request}).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_overall_progress(request):
    """
    全部古建印章收集总览。
    GET /api/stamps/my-overall-progress/
    返回: { collected: 已完全解锁数, total: 总印章数, progress: 百分比, stamps: [...] }
    """
    all_stamps = Stamp.objects.prefetch_related('color_layers').all()
    user_stamps = {
        us.stamp_id: us
        for us in UserStamp.objects.filter(user=request.user).select_related('stamp')
    }

    stamps_data = []
    total = all_stamps.count()
    collected = 0

    for stamp in all_stamps:
        us = user_stamps.get(stamp.id)
        unlocked = us.unlocked_layers if us else 0
        is_complete = unlocked >= stamp.total_layers and stamp.total_layers > 0
        if is_complete:
            collected += 1
        stamps_data.append({
            'stamp_id': stamp.id,
            'name': stamp.name,
            'monument_name': stamp.monument.name if stamp.monument else None,
            'unlocked_layers': unlocked,
            'total_layers': stamp.total_layers,
            'is_complete': is_complete,
        })

    progress = int((collected / total) * 100) if total > 0 else 0
    return Response({
        'collected': collected,
        'total': total,
        'progress': progress,
        'description': f'已集齐 {collected}/{total} 枚印章' if total > 0 else '暂无印章数据',
        'stamps': stamps_data,
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_stamp_for_monument(request, monument_id):
    """获取指定古建对应的用户印章进度"""
    stamp = Stamp.objects.filter(monument_id=monument_id).prefetch_related('color_layers').first()
    if not stamp:
        return Response({'detail': '该古建暂无关联印章。'}, status=404)
    user_stamp, _ = UserStamp.objects.get_or_create(
        user=request.user, stamp=stamp,
        defaults={'unlocked_layers': 0},
    )
    return Response(StampProgressSerializer(user_stamp, context={'request': request}).data)


class StampViewSet(viewsets.ModelViewSet):
    queryset = Stamp.objects.prefetch_related('color_layers').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'monument__name']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return StampWriteSerializer
        return StampSerializer


class StampColorLayerViewSet(viewsets.ModelViewSet):
    queryset = StampColorLayer.objects.select_related('stamp').all()
    serializer_class = StampColorLayerSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        stamp_id = self.request.query_params.get('stamp')
        if stamp_id:
            qs = qs.filter(stamp_id=stamp_id)
        return qs
