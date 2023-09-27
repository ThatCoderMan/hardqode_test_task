from django import forms
from django.contrib import admin

from .models import Lesson, Product, ProductAccess, ViewLesson


class ProductAccessForm(forms.ModelForm):
    class Meta:
        model = ProductAccess
        fields = "__all__"


class ProductAccessInline(admin.TabularInline):
    model = ProductAccess
    form = ProductAccessForm
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "have_access"]
    inlines = [ProductAccessInline]
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"

    def have_access(self, obj):
        return ", ".join([access.user.username for access in obj.users.all()])

    have_access.short_description = "Доступные пользователи"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["name", "video_link", "duration", "products"]
    list_filter = ["product"]
    verbose_name = "Урок"
    verbose_name_plural = "Уроки"

    def products(self, obj):
        return ", ".join([product.name for product in obj.product.all()])

    products.short_description = "Продукты"


@admin.register(ViewLesson)
class ViewLessonAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "viewed_time", "last_view"]
    verbose_name = "Просмотр урока"
    verbose_name_plural = "Просмотры уроков"
