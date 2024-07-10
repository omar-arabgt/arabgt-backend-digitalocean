import logging
from django.db import DatabaseError
from news.models import WpPosts
from .models import Post
from .preprocessing import preprocess_article

logger = logging.getLogger(__name__)

def fetch_and_process_posts(posts):
    new_posts = []
    for post in posts:
        processed_article = preprocess_article(post)

        try:
            wp_post_id = processed_article['post_id']
            wp_post = WpPosts.objects.get(id=wp_post_id)
            new_post = Post(
                post_id=wp_post.id,
                title=processed_article['post_title'],
                content=processed_article['content'],
                publish_date=processed_article['post_date'],
                edit_date=wp_post.post_modified,
                author=wp_post.post_author,
                category="",
                tag=""
            )
            new_post.save()
            new_posts.append(new_post)
        except WpPosts.DoesNotExist:
            logger.error(f"Post with ID {wp_post_id} does not exist.")
            continue
        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            continue

    return new_posts
