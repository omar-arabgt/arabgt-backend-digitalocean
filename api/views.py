from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import time
from .models import Post
from .serializers import PostSerializer
from news.models import WpPosts
from .helpers import fetch_and_process_posts

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class PostListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_fields = ["category", "tag"]

class FetchAndProcessWpPostsView(APIView):
    def get(self, request):
        try:
            start_time = time.time()
            wp_posts = WpPosts.objects.filter(post_type="post", post_status='publish').order_by('-id')[:50].values("id", "post_content", "post_date", "post_title", "post_modified", "post_author")

            if not wp_posts:
                return Response({"error": "No posts found."}, status=status.HTTP_404_NOT_FOUND)

            new_posts = fetch_and_process_posts(wp_posts)

            end_time = time.time()
            response_time = end_time - start_time

            response_data = {
                "done": True,
                "response_time_seconds": response_time,
                "processed_posts": len(new_posts),
                "saved_posts": [post.id for post in new_posts]
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchAndProcessWpPostByIdView(APIView):
    def get(self, request, post_id):
        try:
            start_time = time.time()
            wp_post = WpPosts.objects.filter(id=post_id, post_type="post", post_status='publish').values("id", "post_content", "post_date", "post_title", "post_modified", "post_author").first()

            if not wp_post:
                return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

            new_posts = fetch_and_process_posts([wp_post])

            end_time = time.time()
            response_time = end_time - start_time

            response_data = {
                "done": True,
                "response_time_seconds": response_time,
                "processed_post": new_posts[0].id if new_posts else None,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
