from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('contributor', 'Contributor'),
        ('viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')

    # Add the related_name for user_permissions to avoid conflicts
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # This is the related name you can use
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"



class Content(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class ContentApproval(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approvals")
    status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content.title} - {self.status}"


class SEOData(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    keywords = models.CharField(max_length=255)
    canonical_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.meta_title


class MediaFile(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class ContentTranslation(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)  # e.g., 'en', 'fr', 'es'
    translated_title = models.CharField(max_length=255)
    translated_body = models.TextField()

    def __str__(self):
        return f"{self.content.title} - {self.language}"


class ContentAnalytics(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content.title} - {self.views} Views"


class Integration(models.Model):
    SERVICE_CHOICES = [
        ('google_analytics', 'Google Analytics'),
        ('crm', 'CRM System'),
        ('social_media', 'Social Media API'),
    ]

    name = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SecurityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"


class PerformanceMetrics(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    load_time = models.FloatField()  # in seconds
    cache_status = models.CharField(max_length=50, choices=[('hit', 'Cache Hit'), ('miss', 'Cache Miss')])
    optimized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.content.title} - {self.load_time}s Load Time"
