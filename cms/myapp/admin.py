from django.contrib import admin
from .models import User, Content, ContentApproval, SEOData, MediaFile, ContentTranslation, ContentAnalytics, Integration, SecurityLog, PerformanceMetrics


# Customizing User admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


# Customizing Content admin
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at', 'published_at')
    list_filter = ('status', 'author', 'created_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


# Customizing ContentApproval admin
class ContentApprovalAdmin(admin.ModelAdmin):
    list_display = ('content', 'reviewer', 'status', 'reviewed_at')
    list_filter = ('status', 'reviewer', 'reviewed_at')
    search_fields = ('content__title', 'reviewer__username')


# Customizing SEOData admin
class SEODataAdmin(admin.ModelAdmin):
    list_display = ('content', 'meta_title', 'meta_description', 'keywords', 'canonical_url')
    search_fields = ('content__title', 'meta_title', 'keywords')


# Customizing MediaFile admin
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('content', 'file', 'uploaded_at')
    search_fields = ('content__title', 'file')


# Customizing ContentTranslation admin
class ContentTranslationAdmin(admin.ModelAdmin):
    list_display = ('content', 'language', 'translated_title')
    list_filter = ('language',)
    search_fields = ('content__title', 'language', 'translated_title')


# Customizing ContentAnalytics admin
class ContentAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('content', 'views', 'likes', 'shares', 'last_accessed')
    search_fields = ('content__title',)


# Customizing Integration admin
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


# Customizing SecurityLog admin
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'action', 'ip_address')


# Customizing PerformanceMetrics admin
class PerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ('content', 'load_time', 'cache_status', 'optimized')
    list_filter = ('cache_status', 'optimized')
    search_fields = ('content__title',)


# Register models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(ContentApproval, ContentApprovalAdmin)
admin.site.register(SEOData, SEODataAdmin)
admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(ContentTranslation, ContentTranslationAdmin)
admin.site.register(ContentAnalytics, ContentAnalyticsAdmin)
admin.site.register(Integration, IntegrationAdmin)
admin.site.register(SecurityLog, SecurityLogAdmin)
admin.site.register(PerformanceMetrics, PerformanceMetricsAdmin)
