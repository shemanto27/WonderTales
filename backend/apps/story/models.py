from django.db import models
from apps.users.models import ChildrenProfileModel
# Create your models here.

class StoryModel(models.Model):
    """
    This model is used to store the stories.
    """
    children_profile = models.ForeignKey(ChildrenProfileModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    length = models.IntegerField()
    theme = models.CharField(max_length=100)
    full_story = models.TextField()
    language = models.CharField(max_length=100)
    selected_voices = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

