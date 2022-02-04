from rest_framework import serializers

from chequeapp.models import Check
from chequeapp.services import check_identical_cheques


class CreateCheckSerializer(serializers.Serializer):
    order = serializers.JSONField()

    def create(self, validated_data):
        return Check.objects.create(**validated_data)

    def validate(self, attrs):
        if check_identical_cheques(attrs.get('order').get('id')):
            raise serializers.ValidationError({"error": "Для данного заказа уже созданы чеки"})
        else:
            return attrs


class NewChecksSerializer(serializers.Serializer):
    api_key = serializers.CharField(max_length=100, write_only=True)
    id = serializers.IntegerField(read_only=True)


class CheckSerializer(serializers.Serializer):
    api_key = serializers.CharField(max_length=100, write_only=True)
    check_id = serializers.IntegerField(write_only=True)
    pdf_file = serializers.FileField(read_only=True)
