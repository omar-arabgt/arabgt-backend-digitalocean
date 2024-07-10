import logging
from django.db import DatabaseError, IntegrityError
from news.models import WpPosts, WpTermRelationships, WpTermTaxonomy, WpTerms, WpUsers
from .models import Post
from django.forms.models import model_to_dict
from .preprocessing import preprocess_article

logger = logging.getLogger(__name__)

def fetch_and_process_posts(posts):
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

            new_post = Post(
                post_id=wp_post.id,
                title=processed_article['post_title'],
                content=processed_article['content'],
                publish_date=processed_article['post_date'],
                edit_date=wp_post.post_modified,
                author=author,
                category=categories,
                tag=tags
            )
            logger.info(model_to_dict(new_post))
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
