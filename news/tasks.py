import logging
from celery import shared_task
from django.core.cache import cache

from api.models import Post
from .models import WpPosts, WpTermRelationships, WpTermTaxonomy, WpTerms, WpUsers
from .preprocessing import preprocess_article, get_related_article_ids, preprocess_video_article, normalize_title
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def fetch_and_process_post(post, override_existing=False):
    """
    Fetches and processes a WordPress post and saves/updates it in the database.

    Input:
    - post: A dictionary representing the WordPress post to be processed.
    - override_existing: A boolean flag indicating whether to override existing posts in the database.

    Functionality:
    - Preprocesses the content, fetches related data (author, categories, tags).
    - Creates a new Post if not existing, or updates existing Post based on override_existing flag.

    Output:
    - Logs success or failure.
    """
    try:
        if post["post_type"] == "post" or post["post_type"] == "car_reviews":
            processed_article = preprocess_article(post)
        elif post["post_type"] == "videos":
            processed_article = preprocess_video_article(post)
        else:
            logger.warning(f"Unknown post type {post['post_type']} for post ID {post['id']}")
            return

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
            # Always update or create
            new_post, created = Post.objects.update_or_create(
                post_id=wp_post_id,
                defaults={
                    "title": post["post_title"],
                    "normalized_title": normalize_title(post["post_title"]),
                    "content": processed_article["content"],
                    "publish_date": post["post_date"],
                    "thumbnail": processed_article["thumbnail"],
                    "edit_date": post["post_modified"],
                    "post_type": post["post_type"],
                    "author": author,
                    "category": categories,
                    "tag": tags,
                    "modify_date": post["post_modified"],
                }
            )
        else:
            # First check if post already exists
            if Post.objects.filter(post_id=wp_post_id).exists():
                logger.info(f"Post {wp_post_id} already exists. Skipping creation as override_existing=False.")
                return  # Skip without error
            else:
                new_post = Post.objects.create(
                    post_id=wp_post_id,
                    title=post["post_title"],
                    normalized_title=normalize_title(post["post_title"]),
                    content=processed_article["content"],
                    publish_date=post["post_date"],
                    thumbnail=processed_article["thumbnail"],
                    edit_date=post["post_modified"],
                    post_type=post["post_type"],
                    author=author,
                    category=categories,
                    tag=tags,
                    modify_date=post["post_modified"],
                )

        # # Process related articles if they exist
        # related_articles = processed_article.get("related_articles")
        # if related_articles:
        #     related_ids = get_related_article_ids(related_articles)
        #     new_post.related_articles.add(*related_ids)

        # Clear homepage cache if exists
        try:
            cache_client = cache._cache.get_client()
            keys = cache_client.keys("*home_page_view_cache*")
            if keys:
                cache_client.delete(*keys)
        except Exception as e:
            logger.error(f"Error while deleting cache: {str(e)}")

        logger.info(f"Post {new_post.id} - {new_post.post_id} processed successfully!")

    except Exception as e:
        logger.error(f"Error while processing post {post.get('id', 'unknown')}: {str(e)}")



@shared_task
def fetch_and_process_wp_posts(post_id=None, override_all=False):
    """
    Fetches and processes published WordPress posts.

    Input:
    - post_id: An integer representing the ID of the WordPress post to be processed.
               Processes all posts if post_id is None.
    - override_all: A boolean to indicate if all posts should be processed
                    regardless of modification date.

    Functionality:
    - Fetches all published WordPress posts.
    - Processes each post and saves it to the database.
    - Additionally, re-processes any post modified within the last 30 days.

    Output:
    - Returns a dictionary containing:
      - done: A boolean indicating the operation completion status.
      - processed_posts: The number of processed posts.
      - saved_posts: A list of IDs of the saved posts.
    """
    # Determine if we should override existing posts
    override_existing = bool(post_id or override_all)

    query_filter = {
        "post_type__in": ["post", "videos", "car_reviews"],
        "post_status": "publish",
    }

    # If a specific post ID is provided, filter by that ID and override
    if post_id:
        query_filter["id"] = post_id
    elif not override_all:
        # Only retrieve posts modified after the latest saved post's date
        latest_post = Post.objects.order_by("modify_date").last()
        if latest_post:
            query_filter["post_modified__gt"] = latest_post.modify_date

    # Fetch posts from WordPress (normal logic)
    wp_posts = WpPosts.objects.filter(**query_filter).values(
        "id", "post_content", "post_date", "post_title",
        "post_modified", "post_author", "post_type"
    )

    # If no posts are found, log and return an error message
    if not wp_posts:
        logger.info("No posts found.")
        return {"error": "No posts found."}

    # Process each fetched post asynchronously (normal logic)
    for wp_post in wp_posts:
        fetch_and_process_post.delay(wp_post, override_existing)

    # --- NEW LOGIC: Fetch posts modified within last 30 days ---
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_modified_posts = WpPosts.objects.filter(
        post_type__in=["post", "videos", "car_reviews"],
        post_status="publish",
        post_modified__gte=thirty_days_ago
    ).values(
        "id", "post_content", "post_date", "post_title",
        "post_modified", "post_author", "post_type"
    )

    # Process each recently modified post asynchronously with override_existing=True
    if recent_modified_posts:
        for wp_post in recent_modified_posts:
            fetch_and_process_post.delay(wp_post, override_existing=True)

    return {"success": f"Processing {len(wp_posts)} posts and {len(recent_modified_posts)} recently modified posts."}


