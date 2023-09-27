from education.models import Product, ProductAccess, ViewLesson
from rest_framework.generics import ListAPIView

from .permissions import HasAccessPermission
from .serializers import (ProductLessonViewSerializer, ProductSerializer,
                          StatisticSerializer)


class UserLessonsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.kwargs["user"]
        return ProductAccess.objects.filter(user=user)


class UserProductLessonsView(ListAPIView):
    permission_classes = [HasAccessPermission]
    serializer_class = ProductLessonViewSerializer

    def get_queryset(self):
        user = self.kwargs["user"]
        product = self.kwargs["product"]
        return ViewLesson.objects.filter(user=user, lesson__product=product)


class ProductStatisticsView(ListAPIView):
    serializer_class = StatisticSerializer
    queryset = Product.objects.all()
