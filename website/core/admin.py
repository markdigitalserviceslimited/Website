from django.contrib import admin
from .models import QuoteRequest, Service, CaseStudy, FAQ


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'business_name', 'service_needed', 'email', 'phone_or_whatsapp', 'estimated_budget', 'status', 'created_at')
    list_filter = ('service_needed', 'status', 'created_at')
    search_fields = ('full_name', 'business_name', 'email', 'phone_or_whatsapp', 'project_description')
    list_editable = ('status',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'target_audience', 'key_benefit', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'short_description')


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'title', 'milestone_stat', 'category', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'category')
    search_fields = ('client_name', 'title', 'outcome')
    list_editable = ('is_featured',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')
