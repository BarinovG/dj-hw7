from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию. # Текущий пользователь является создателем объявления
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        advs_count = self.Meta.model.objects.filter(creator=self.context["request"].user,
                                                    status=AdvertisementStatusChoices.OPEN).count()
        if advs_count > 9 and self.context["request"].method == "POST":
            raise ValidationError('Нельзя создать больше 10 объявлений')
        return data