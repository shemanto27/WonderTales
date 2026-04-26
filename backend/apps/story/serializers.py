from rest_framework import serializers
from apps.story.models import StoryModel

class StoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryModel
        fields = [
            'id', 'children_profile', 'title', 'length', 'theme', 
            'full_story', 'language', 'selected_voices', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']