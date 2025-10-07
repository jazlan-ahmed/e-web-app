from django.contrib import admin
from .models import Product, Category, SupportRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "category", "offerPrice", "currency", "views")
    list_filter = ("company", "category", "currency")
    search_fields = ("name", "company", "description")

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at")
    search_fields = ("subject", "name", "email", "message")
    ordering = ("-created_at",)
