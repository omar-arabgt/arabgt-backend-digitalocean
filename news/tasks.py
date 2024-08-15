import logging
from celery import shared_task

from api.models import Post
from .models import WpPosts, WpTermRelationships, WpTermTaxonomy, WpTerms, WpUsers
from .preprocessing import preprocess_article, get_related_article_ids, preprocess_video_article

logger = logging.getLogger(__name__)


@shared_task
def fetch_and_process_post(post, override_existing=False):
    """
    Fetches and processes a list of posts.

    Input:
    - posts: A list of dictionaries representing the WordPress posts to be processed.
    - override_existing: A boolean flag indicating whether to override existing posts in the database.

    Functionality:
    - Iterates over each post, preprocesses the content, and fetches related data from WordPress models.
    - Creates or updates the Post object in the database.

    Output:
    - Returns a list of saved Post objects.
    """
    if post["post_type"] == "post" or post["post_type"] == "car_reviews":
        processed_article = preprocess_article(post)
    elif post["post_type"] == "videos":
        processed_article = preprocess_video_article(post)

    try:
        wp_post_id = post["id"]
        wp_author = WpUsers.objects.get(id=post["post_author"])
        author = wp_author.display_name

        term_relations = WpTermRelationships.objects.filter(object_id=wp_post_id)
        
        categories = []
        tags = []

        for term_relation in term_relations:
            term_taxonomy = WpTermTaxonomy.objects.get(term_taxonomy_id=term_relation.term_taxonomy_id)
            term = WpTerms.objects.get(term_id=term_taxonomy.term_id)

            if term_taxonomy.taxonomy == "category":
                categories.append(term.name)
            elif term_taxonomy.taxonomy == "post_tag":
                tags.append(term.name)

        if override_existing:
            new_post, created = Post.objects.update_or_create(
                post_id=wp_post_id,
                defaults={
                    "title": post["post_title"],
                    "content": processed_article["content"],
                    "publish_date": post["post_date"],
                    "thumbnail": processed_article["thumbnail"],
                    "edit_date": post["post_modified"],
                    "post_type": post["post_type"],
                    "author": author,
                    "category": categories,
                    "tag": tags
                }
            )
        else:
            new_post = Post.objects.create(
                post_id=wp_post_id,
                title=post["post_title"],
                content=processed_article["content"],
                publish_date=post["post_date"],
                thumbnail=processed_article["thumbnail"],
                edit_date=post["post_modified"],
                post_type=post["post_type"],
                author=author,
                category=categories,
                tag=tags
            )

        related_articles = processed_article.get("related_articles")
        if related_articles:
            related_ids = get_related_article_ids(related_articles)
            new_post.related_articles.add(*related_ids)

        logger.info(f"Post {new_post.id} - {new_post.post_id} processed succesfully!")
    except Exception as e:
        logger.error(f"Error while processing post {wp_post_id}: {str(e)}")


@shared_task
def fetch_and_process_wp_posts(post_id=None):
    """
    Fetches and processes published WordPress posts.

    Input:
    - post_id: An integer representing the ID of the WordPress post to be processed.
               It process all posts if post_id is None 

    Functionality:
    - Fetches all published WordPress posts.
    - Processes each post and saves it to the database.

    Output:
    - Returns a dictionary containing:
      - done: A boolean indicating the operation completion status.
      - processed_posts: The number of processed posts.
      - saved_posts: A list of IDs of the saved posts.
    """
    override_existing = False
    query_filter = {
        "post_type__in": ["post", "videos", "car_reviews"],
        "post_status": "publish",
    }

    if post_id:
        query_filter["id"] = post_id
        override_existing = True
    else:
        #  check latest post id on postgres and retrieve new posts from mysql
        latest_post = Post.objects.order_by("post_id").last()
        if latest_post:
            query_filter["id__gt"] = latest_post.post_id

    wp_posts = WpPosts.objects.filter(**query_filter).values("id", "post_content", "post_date", "post_title", "post_modified", "post_author", "post_type")

    if not wp_posts:
        logger.info("No posts found.")
        return {"error": "No posts found."}

    for wp_post in wp_posts:
        fetch_and_process_post.delay(wp_post, override_existing)

    return {"success": f"Processing {len(wp_posts)} posts..."}
