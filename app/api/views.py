from education.models import Product, ProductAccess, ViewLesson
from rest_framework.generics import ListAPIView

from .permissions import HasAccessPermission
from .serializers import (ProductLessonViewSerializer, ProductSerializer,
                          StatisticSerializer)


class UserLessonsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.kwargs["user"]
        return ProductAccess.objects.filter(
            user__username=user
        ).prefetch_related("product__lessons")


class UserProductLessonsView(ListAPIView):
    permission_classes = [HasAccessPermission]
    serializer_class = ProductLessonViewSerializer

    def get_queryset(self):
        user = self.kwargs["user"]
        product = self.kwargs["product"]
        return ViewLesson.objects.filter(
            user__username=user, lesson__product__name=product
        ).prefetch_related("lesson")


class ProductStatisticsView(ListAPIView):
    serializer_class = StatisticSerializer
    queryset = Product.objects.all().prefetch_related("lessons")
