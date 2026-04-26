from rest_framework.viewsets import ModelViewSet
from apps.story.models import StoryModel
from apps.story.serializers import StoryModelSerializer
from rest_framework.permissions import IsAuthenticated

class StoryModelViewSet(ModelViewSet):
    queryset = StoryModel.objects.all()
    serializer_class = StoryModelSerializer
    permission_classes = [IsAuthenticated]
    

# Create your views here.
