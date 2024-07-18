from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .models import Post
from .serializers import PostSerializer
from .filters import PostFilter 

class PostView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_class = PostFilter
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
