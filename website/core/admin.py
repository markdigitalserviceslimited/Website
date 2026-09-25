from django.contrib import admin
from django.utils.html import format_html
from .models import (
    QuoteRequest, Service, CaseStudy, FAQ,
    BlogCategory, BlogPost, Testimonial,
    BlogAuthor, AuthorSocialLink
)


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


class AuthorSocialLinkInline(admin.TabularInline):
    model = AuthorSocialLink
    extra = 1
    fields = ('platform', 'url', 'order')


@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_or_title', 'article_count', 'social_links_count', 'avatar_preview', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'role_or_title', 'bio')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)
    inlines = (AuthorSocialLinkInline,)
    fieldsets = (
        ('Author Information', {
            'fields': ('name', 'slug', 'role_or_title', 'bio', 'is_active')
        }),
        ('Profile Media', {
            'fields': ('avatar_image', 'avatar_initial')
        }),
    )

    def article_count(self, obj):
        return obj.posts.count()
    article_count.short_description = "Articles"

    def social_links_count(self, obj):
        return obj.social_links.count()
    social_links_count.short_description = "Social Links"

    def avatar_preview(self, obj):
        if obj.avatar_image:
            return format_html('<img src="{}" style="height: 34px; width: 34px; border-radius: 50%; object-fit: cover;" />', obj.avatar_image.url)
        return format_html('<span style="display:inline-block; width:30px; height:30px; line-height:30px; text-align:center; background:#032678; color:white; border-radius:50%; font-size:11px; font-weight:bold;">{}</span>', obj.avatar_initial)
    avatar_preview.short_description = "Avatar"


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Articles"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'author_name', 'status', 'featured', 'view_count', 'publish_date', 'image_preview')
    list_filter = ('status', 'featured', 'category', 'author', 'publish_date')
    search_fields = ('title', 'excerpt', 'content', 'author_name', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'featured')
    date_hierarchy = 'publish_date'
    fieldsets = (
        ('Article Details', {
            'fields': ('title', 'slug', 'category', 'author', 'author_name', 'read_time', 'status', 'featured', 'publish_date')
        }),
        ('Featured Media', {
            'fields': ('featured_image', 'featured_image_alt')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Search Engine Optimization (SEO)', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
    )

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="height: 38px; width: 60px; object-fit: cover; border-radius: 4px;" />', obj.featured_image.url)
        return "—"
    image_preview.short_description = "Thumbnail"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'organization', 'service_category', 'rating', 'verified', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'verified', 'rating')
    search_fields = ('client_name', 'organization', 'service_category', 'quote')
    list_editable = ('order', 'is_active', 'verified')


