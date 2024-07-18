import logging
import time
from django.db import DatabaseError, IntegrityError
from news.models import WpPosts, WpTermRelationships, WpTermTaxonomy, WpTerms, WpUsers
from .models import Post
from .preprocessing import preprocess_article, update_related_article_ids

logger = logging.getLogger(__name__)

def fetch_and_process_posts(posts, override_existing=False):
    saved_posts = []
    for post in posts:
        processed_article = preprocess_article(post)

        try:
            wp_post_id = processed_article['post_id']
            wp_post = WpPosts.objects.get(id=wp_post_id)
            wp_author = WpUsers.objects.get(id=wp_post.post_author)
            author = wp_author.display_name

            term_relations = WpTermRelationships.objects.filter(object_id=wp_post_id)
            
            categories = []
            tags = []

            for term_relation in term_relations:
                term_taxonomy = WpTermTaxonomy.objects.get(term_taxonomy_id=term_relation.term_taxonomy_id)
                term = WpTerms.objects.get(term_id=term_taxonomy.term_id)

                if term_taxonomy.taxonomy == 'category':
                    categories.append(term.name)
                elif term_taxonomy.taxonomy == 'post_tag':
                    tags.append(term.name)

            if override_existing:
                new_post, created = Post.objects.update_or_create(
                    post_id=wp_post.id,
                    defaults={
                        'title': processed_article['post_title'],
                        'content': processed_article['content'],
                        'publish_date': processed_article['post_date'],
                        'thumbnail': processed_article['thumbnail'],
                        'related_articles': processed_article['related_articles'],
                        'edit_date': wp_post.post_modified,
                        'author': author,
                        'category': categories,
                        'tag': tags
                    }
                )
            else:
                new_post = Post(
                    post_id=wp_post.id,
                    title=processed_article['post_title'],
                    content=processed_article['content'],
                    publish_date=processed_article['post_date'],
                    thumbnail=processed_article['thumbnail'],
                    related_articles=processed_article['related_articles'],
                    edit_date=wp_post.post_modified,
                    author=author,
                    category=categories,
                    tag=tags
                )
                new_post.save()
            saved_posts.append(new_post)
        except WpPosts.DoesNotExist:
            logger.error(f"Post with ID {wp_post_id} does not exist.")
            continue
        except WpUsers.DoesNotExist:
            logger.error(f"User with ID {wp_post.post_author} does not exist.")
            continue
        except IntegrityError as e:
            logger.error(f"Integrity error: {e}")
            continue
        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            continue

    return saved_posts

def fetch_and_process_all_wp_posts():
    try:
        start_time = time.time()
        wp_posts = WpPosts.objects.filter(post_type="post", post_status='publish').values("id", "post_content", "post_date", "post_title", "post_modified", "post_author")

        if not wp_posts:
            logger.error("No posts found.")
            return {"error": "No posts found."}

        new_posts = fetch_and_process_posts(wp_posts)

        end_time = time.time()
        response_time = end_time - start_time

        response_data = {
            "done": True,
            "response_time_seconds": response_time,
            "processed_posts": len(new_posts),
            "saved_posts": [post.id for post in new_posts]
        }
        return response_data

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": "An internal error occurred."}

def fetch_and_process_wp_post_by_id(post_id):
    try:
        start_time = time.time()
        wp_post = WpPosts.objects.filter(id=post_id, post_type="post", post_status='publish').values("id", "post_content", "post_date", "post_title", "post_modified", "post_author").first()

        if not wp_post:
            logger.error("Post not found.")
            return {"error": "Post not found."}

        new_posts = fetch_and_process_posts([wp_post], True)

        end_time = time.time()
        response_time = end_time - start_time

        response_data = {
            "done": True,
            "response_time_seconds": response_time,
            "processed_post": new_posts[0].id if new_posts else None,
        }
        return response_data

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": "An internal error occurred."}

def fetch_and_update_related_articles_ids():
    try:
        posts = Post.objects.all()

        if not posts:
            return {"error": "No posts found."}
        
        updated_posts = []
        missing_titles = []

        for post in posts:
            updated_post, missing = update_related_article_ids(post)
            post.content = updated_post.content
            post.save()
            updated_posts.append(post.id)
            if missing:
                missing_titles.extend(missing)

        response_data = {
            "done": True,
            "processed_posts": len(updated_posts),
            "missing_titles": missing_titles
        }
        return response_data
    
    except Exception as e:
        return {"error": f"An internal error occurred: {e}"}

def fetch_and_update_related_articles_ids_by_id(id):
    try:
        start_time = time.time()
        
        post = Post.objects.filter(id=id).first()
        
        if not post:
            return {"error": "Post not found."}

        updated_post, missing_titles = update_related_article_ids(post)
        post.content = updated_post.content
        post.save()

        end_time = time.time()
        response_time = end_time - start_time

        response_data = {
            "done": True,
            "response_time_seconds": response_time,
            "processed_posts": 1,
            "missing_titles": missing_titles,
        }
        return response_data
    
    except Exception as e:
        return {"error": f"An internal error occurred: {e}"}
