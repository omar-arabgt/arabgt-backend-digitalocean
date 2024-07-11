from rest_framework.generics import ListAPIView
import logging
from .models import Post
from .serializers import PostSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class PostListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_fields = ["category", "tag"]
