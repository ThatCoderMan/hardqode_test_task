from django.urls import path

from .views import (ProductStatisticsView, UserLessonsView,
                    UserProductLessonsView)

urlpatterns = [
    path(
        "lessons/<str:user>/",
        UserLessonsView.as_view(),
        name="user-products"
    ),
    path(
        "lessons/<str:user>/<str:product>",
        UserProductLessonsView.as_view(),
        name="user-lessons",
    ),
    path(
        "statistics/",
        ProductStatisticsView.as_view(),
        name="statistics"
    ),
]
