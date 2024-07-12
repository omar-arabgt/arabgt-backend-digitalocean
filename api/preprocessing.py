import re
from bs4 import BeautifulSoup
from news.models import WpPosts, WpPostmeta
from .models import Post
import ast
import urllib.parse
from django.db.models import Q

def extract_elements(element):
    elements = []
    text_buffer = []
    external_links = []

    def add_text_buffer_to_elements():
        if text_buffer:
            text = ''.join(text_buffer).strip()
            if text:  # Only add if the text is not empty
                elements.append({
                    "text": text,
                    "media": {},
                    "heading": ""
                })
            text_buffer.clear()

    def handle_strong_tag(child):
        text = child.get_text(strip=True)
        if (child.previous_sibling and '\n' in child.previous_sibling) or (child.next_sibling and '\n' in child.next_sibling):
            add_text_buffer_to_elements()
            elements.append({
                "media": {},
                "heading": text,
                "text": "",
            })
        else:
            text_buffer.append(text)

    for child in element.children:
        if isinstance(child, str):
            text_buffer.append(child)
        else:
            tag_name = child.name
            attributes = child.attrs
            text = child.get_text(strip=True)

            if tag_name == 'strong':
                handle_strong_tag(child)
            elif tag_name == 'a':
                href = attributes.get('href', '')
                if href:
                    external_links.append(href)
                if child.find('strong') and (
                    (child.previous_sibling is None or (isinstance(child.previous_sibling, str) and child.previous_sibling.strip() == "")) or
                    (child.next_sibling is None or (isinstance(child.next_sibling, str) and child.next_sibling.strip() == ""))
                ):
                    add_text_buffer_to_elements()
                    elements.append({
                        "text": "",
                        "media": {},
                        "heading": text
                    })
                else:
                    text_buffer.append(child.get_text())  # Append the text directly
            elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                add_text_buffer_to_elements()
                elements.append({
                    "text": "",
                    "media": {},
                    "heading": text
                })
            elif tag_name in ['ul', 'ol']:
                add_text_buffer_to_elements()
                bullets = "\n".join([f"• {li.get_text(strip=True)}" for li in child.find_all('li')])
                elements.append({
                    "text": bullets,
                    "media": {},
                    "heading": ""
                })
            elif tag_name == 'iframe':
                add_text_buffer_to_elements()
                src = attributes.get('src', '')
                if 'youtube' in src:
                    youtube_id = re.search(r"embed/([^?]+)", src).group(1)
                    elements.append({
                        "text": "",
                        "media": {"youtube": f"https://www.youtube.com/watch?v={youtube_id}"},
                        "heading": ""
                    })
                else:
                    elements.append({
                        "text": "",
                        "media": {"iframe": src},
                        "heading": ""
                    })
            elif tag_name == 'img':
                add_text_buffer_to_elements()
                src = attributes.get('src', '')
                elements.append({
                    "text": "",
                    "media": {"image": src},
                    "heading": ""
                })
            else:
                add_text_buffer_to_elements()
                elements.append({
                    "text": text,
                    "media": {},
                    "heading": ""
                })

    add_text_buffer_to_elements()

    # Remove any empty dictionary items
    elements = [element for element in elements if element['text'] or element['media'] or element['heading']]

    return elements, external_links

def handle_galleries(text):
    elements = []
    parts = re.split(r'(\[gallery[^\]]*\])', text)
    for part in parts:
        if part.startswith('[gallery'):
            gallery_ids_match = re.search(r'ids="([\d,]+)"', part)
            if gallery_ids_match:
                gallery_ids = gallery_ids_match.group(1).split(',')
                elements.append({"text": "", "media": {"gallery": gallery_ids}, "heading": ""})
        else:
            if part.strip():
                elements.append({"text": part.strip(), "media": {}, "heading": ""})
    
    return elements

def replace_gallery_ids_with_links(elements):
    gallery_ids = []
    for element in elements:
        if 'gallery' in element['media']:
            gallery_ids.extend(element['media']['gallery'])

    wp_posts = WpPosts.objects.filter(post_type="attachment", id__in=gallery_ids)
    wp_posts_dict = {str(post.id): post.guid for post in wp_posts}

    updated_elements = []
    for element in elements:
        if 'gallery' in element['media']:
            ids = element['media']['gallery']
            links = [wp_posts_dict.get(id, '') for id in ids]
            element['media'] = {"gallery": links}
        updated_elements.append(element)
    
    return updated_elements

def get_thumbnail(post_id):
    thumbnail_id = WpPostmeta.objects.filter(post_id=post_id, meta_key='_thumbnail_id').values_list('meta_value', flat=True).first()
    thumbnail_url = None
    if thumbnail_id:
        thumbnail_url = WpPostmeta.objects.filter(post_id=thumbnail_id, meta_key='_wp_attached_file').values_list('meta_value', flat=True).first()
    
    return thumbnail_url

def process_external_links(external_links):
    related_articles = []
    cleaned_external_links = []
    
    for link in external_links:
        if "arabgt.com" in link:
            decoded_link = urllib.parse.unquote(link)
            parts = decoded_link.split('/')
            if len(parts) > 0:
                wp_post_link_name = parts[-2]
                formatted_part = wp_post_link_name.replace('-', ' ')
                related_articles.append({"link": decoded_link, "title": formatted_part})
        else:
            cleaned_external_links.append(link)
    
    return related_articles, cleaned_external_links

def normalize_title(title):
    title = title.lower()
    title = re.sub(r'[\-\–]', ' ', title)
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def update_related_article_ids(post):
    try:
        content = ast.literal_eval(post.content)
    except (SyntaxError, ValueError) as e:
        return post, []

    updated = False
    missing_titles = [] 
    for element in content:
        if isinstance(element, dict) and 'related_articles' in element:
            related_articles = element.get("related_articles", [])
            for related_article in related_articles:
                title = related_article.get('title')
                if title:
                    normalized_title = normalize_title(title)
                    words = normalized_title.split()
                    query = Q()
                    for word in words:
                        query &= Q(title__icontains=word)
                    related_post = Post.objects.filter(query).first()
                    if related_post:
                        related_article['id'] = related_post.id
                        updated = True
                    else:
                        missing_titles.append(title)

    if updated:
        post.content = str(content)

    return post, missing_titles


def preprocess_article(article):
    post_content = article['post_content']
    post_id = article['id']
    post_date = article['post_date']
    post_title = article['post_title']

    soup = BeautifulSoup(post_content, "html.parser")
    structured_data, external_links = extract_elements(soup.body if soup.body else soup)

    final_elements = []
    for element in structured_data:
        if '[gallery' in element.get('text', ''):
            final_elements.extend(handle_galleries(element['text']))
        else:
            final_elements.append(element)

    final_elements = replace_gallery_ids_with_links(final_elements)
    
    related_articles, cleaned_external_links = process_external_links(external_links)

    if related_articles:
        final_elements.append({
            "related_articles": related_articles
        })

    if cleaned_external_links:
        final_elements.append({
            "external_links": cleaned_external_links
        })
        
    thumbnail_url = get_thumbnail(post_id)
    if thumbnail_url:
        final_elements.append({
            "thumbnail": f'https://arabgt.com/wp-content/uploads/{thumbnail_url}'
        })

    output_data = {
        "post_date": post_date,
        "post_content": post_content,
        "post_title": post_title,
        "post_id": post_id,
        "content": final_elements
    }
    
    return output_data
