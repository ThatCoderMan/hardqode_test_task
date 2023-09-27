from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver


class Product(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Владелец продукта",
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
        help_text="Название продукта",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductAccess(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь с доступом к продукту",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Продукт",
        help_text="Продукт, к которому есть доступ",
    )

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Доступ к продукту"
        verbose_name_plural = "Доступы к продуктам"

    def __str__(self):
        return f"{self.user} имеет доступ к {self.product}"


class Lesson(models.Model):
    product = models.ManyToManyField(
        Product,
        related_name="lessons",
        verbose_name="Продукты",
        help_text="Продукты, в которых содержится урок",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Название урока"
    )
    video_link = models.URLField(
        unique=True,
        verbose_name="Ссылка на видео",
        help_text="Ссылка на видео урока"
    )
    duration = models.DurationField(
        verbose_name="Длительность",
        help_text="Длительность просмотра урока (в секундах)",
    )

    @property
    def duration_seconds(self) -> int:
        return int(self.duration.total_seconds())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class ViewLesson(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, просмотревший урок",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Урок",
        help_text="Урок, просмотренный пользователем",
    )
    viewed_time = models.DurationField(
        default=timedelta,
        verbose_name="Время просмотра",
        help_text="Общее время просмотра урока",
    )
    last_view = models.DateField(
        auto_now=True,
        verbose_name="Дата последнего просмотра",
        help_text="Дата последнего просмотра урока",
    )

    @property
    def viewed_seconds(self) -> int:
        return int(self.viewed_time.total_seconds())

    @property
    def status(self) -> str:
        if self._calculate_viewed_percentage() >= 0.8:
            return "Просмотрено"
        return "Не просмотрено"

    def _calculate_viewed_percentage(self):
        total_time = self.lesson.duration_seconds
        viewed_time = self.viewed_seconds
        return viewed_time / total_time

    def __str__(self):
        return (
            f"{self.user} просмотрел {self.viewed_seconds} секунд "
            f"урока {self.lesson}"
        )

    class Meta:
        unique_together = ("user", "lesson")
        verbose_name = "Просмотр урока"
        verbose_name_plural = "Просмотры уроков"


@receiver(m2m_changed, sender=Lesson.product.through)
def create_lesson_views(instance, action, **kwargs):
    if action != "post_add":
        return
    products = instance.product.all()
    users = set(User.objects.filter(productaccess__product__in=products).all())
    existing_views = ViewLesson.objects.filter(lesson=instance)
    for view in existing_views:
        if view.user not in users:
            view.delete()
    existing_users = ViewLesson.objects.filter(
        user__in=users, lesson=instance
    ).values_list("user", flat=True)
    new_views = []
    for user in users:
        if user.id not in existing_users:
            new_views.append(ViewLesson(user=user, lesson=instance))
    ViewLesson.objects.bulk_create(new_views)


@receiver(post_save, sender=ProductAccess)
def create_user_views(instance, **kwargs):
    user = instance.user
    lessons = instance.product.lessons.get_queryset()
    existing_lessons = ViewLesson.objects.filter(
        user=user, lesson__in=lessons
    ).values_list("lesson__id", flat=True)
    new_views = []
    for lesson in lessons:
        if lesson.id not in existing_lessons:
            new_views.append(ViewLesson(user=user, lesson=lesson))
    ViewLesson.objects.bulk_create(new_views)


@receiver(pre_delete, sender=ProductAccess)
def delete_user_views(instance, **kwargs):
    user = instance.user
    lessons = instance.product.lessons.get_queryset()
    for view in ViewLesson.objects.filter(user=user, lesson__in=lessons):
        view.delete()
