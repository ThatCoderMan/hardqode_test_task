import datetime

from django.contrib.auth.models import User
from django.db.models import F, Sum
from drf_yasg.utils import swagger_serializer_method
from education.models import Product, ProductAccess, ViewLesson
from rest_framework import serializers


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewLesson
        fields = ["lesson", "status", "viewed_seconds"]


class ProductSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    @swagger_serializer_method(
        serializer_or_field=LessonViewSerializer(many=True)
    )
    def get_lessons(self, obj):
        lessons = ViewLesson.objects.filter(
                user=obj.user,
                lesson__product=obj.product
        ).prefetch_related("lesson").all()
        return LessonViewSerializer(lessons, many=True).data

    class Meta:
        model = ProductAccess
        fields = ["product", "lessons"]


class ProductLessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewLesson
        fields = ["lesson", "status", "viewed_seconds", "last_view"]


class StatisticSerializer(serializers.ModelSerializer):
    lessons_viewed = serializers.SerializerMethodField()
    total_viewed_time = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    acquisition_percentage = serializers.SerializerMethodField()

    def get_lessons_viewed(self, obj) -> int:
        return ViewLesson.objects.filter(
            lesson__product=obj, viewed_time__gte=F("lesson__duration") * 0.8
        ).count()

    def get_total_viewed_time(self, obj) -> int:
        total_time = ViewLesson.objects.filter(lesson__product=obj).aggregate(
            Sum("viewed_time")
        )
        viewed_time = total_time["viewed_time__sum"]
        if isinstance(viewed_time, datetime.timedelta):
            return int(viewed_time.total_seconds())
        return 0

    def get_total_students(self, obj) -> int:
        return obj.users.count()

    def get_acquisition_percentage(self, obj) -> int:
        total_users = User.objects.count()
        product_access_count = ProductAccess.objects.filter(
            product=obj
        ).count()
        return (product_access_count / total_users) * 100 if total_users else 0

    class Meta:
        model = Product
        fields = [
            "name",
            "lessons_viewed",
            "total_viewed_time",
            "total_students",
            "acquisition_percentage",
        ]
