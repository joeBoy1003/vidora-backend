from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

class VideoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = VideoManager()  # Default manager that excludes soft-deleted records
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def save(self, *args, **kwargs):
        # Save the video instance first to ensure video_file has a path
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_user_permissions")