from rest_framework.generics import ListAPIView

from .models import Post
from .serializers import PostSerializer


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_fields = ["category", "tag"]
