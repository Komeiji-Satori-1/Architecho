from rest_framework import serializers
from .models import Stamp, StampColorLayer, UserStamp


class StampColorLayerSerializer(serializers.ModelSerializer):
    svg_url = serializers.SerializerMethodField()

    class Meta:
        model = StampColorLayer
        fields = ['id', 'stamp', 'layer_index', 'layer_name', 'color', 'svg_file', 'svg_url', 'blend_mode']
        read_only_fields = ['id']

    def get_svg_url(self, obj):
        request = self.context.get('request')
        if obj.svg_file and request:
            return request.build_absolute_uri(obj.svg_file.url)
        return None


class StampSerializer(serializers.ModelSerializer):
    color_layers = StampColorLayerSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Stamp
        fields = ['id', 'name', 'image', 'image_url', 'monument', 'total_layers', 'color_layers', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class StampWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['name', 'image', 'monument', 'total_layers']


class StampProgressSerializer(serializers.Serializer):
    stamp_id = serializers.IntegerField(source='stamp.id')
    title = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    collected = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    color_layers = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.stamp.name

    def get_progress(self, obj):
        total = obj.stamp.total_layers
        if total == 0:
            return 0
        return int((obj.unlocked_layers / total) * 100)

    def get_collected(self, obj):
        return obj.unlocked_layers

    def get_total(self, obj):
        return obj.stamp.total_layers

    def get_description(self, obj):
        remaining = obj.stamp.total_layers - obj.unlocked_layers
        if remaining <= 0:
            return f'恭喜！你已完全解锁「{obj.stamp.name}」印章。'
        return (
            f'距离完全解锁「{obj.stamp.name}」还需再答对 {remaining} 道题目。'
            f'每次答对均可解锁一层新的套色。'
        )

    def get_color_layers(self, obj):
        layers = obj.stamp.color_layers.all()
        request = self.context.get('request')
        return StampColorLayerSerializer(layers, many=True, context={'request': request}).data
