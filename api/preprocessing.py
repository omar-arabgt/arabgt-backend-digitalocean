import re
from bs4 import BeautifulSoup
from news.models import WpPosts
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def extract_elements(element):
    elements = []
    text_buffer = []

    for child in element.children:
        if isinstance(child, str):
            text_buffer.append(child.strip())
        else:
            tag_name = child.name
            attributes = child.attrs
            text = child.get_text(strip=True)

            if tag_name in ['a', 'strong']:
                if tag_name == 'strong' and (child.previous_sibling and '\n' in child.previous_sibling or child.next_sibling and '\n' in child.next_sibling):
                    elements.append({
                        "media": "",
                        "text": text,
                        "heading": "",
                        "bold": True
                    })
                else:
                    text_buffer.append(text)
            else:
                if text_buffer:
                    elements.append({
                        "text": ' '.join(text_buffer),
                        "media": "",
                        "heading": ""
                    })
                    text_buffer = []

                if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    element_data = {
                        "text": "",
                        "media": "",
                        "heading": text
                    }
                elif tag_name == 'strong':
                    element_data = {
                        "text": text,
                        "media": "",
                        "heading": "",
                        "bold": True
                    }
                elif tag_name in ['ul', 'ol']:
                    bullets = "\n".join([f"• {li.get_text(strip=True)}" for li in child.find_all('li')])
                    element_data = {
                        "text": bullets,
                        "media": "",
                        "heading": ""
                    }
                elif tag_name == 'iframe':
                    src = attributes.get('src', '')
                    if 'youtube' in src:
                        youtube_id = re.search(r"embed/([^?]+)", src).group(1)
                        element_data = {
                            "text": "",
                            "media": f"https://www.youtube.com/watch?v={youtube_id}",
                            "heading": ""
                        }
                    else:
                        element_data = {
                            "text": "",
                            "media": f"iframe {src}",
                            "heading": ""
                        }
                elif tag_name == 'img':
                    src = attributes.get('src', '')
                    element_data = {
                        "text": "",
                        "media": f"[Image: {src}]",
                        "heading": ""
                    }
                else:
                    element_data = {
                        "text": text,
                        "media": "",
                        "heading": ""
                    }
                elements.append(element_data)

    if text_buffer:
        elements.append({
            "text": ' '.join(text_buffer),
            "media": "",
            "heading": ""
        })

    return elements

def handle_galleries(text):
    elements = []
    parts = re.split(r'(\[gallery[^\]]*\])', text)
    for part in parts:
        if part.startswith('[gallery'):
            elements.append({"text": "", "media": part, "heading": ""})
        else:
            if part.strip():
                elements.append({"text": part.strip(), "media": "", "heading": ""})
    return elements

def replace_gallery_ids_with_links(elements):
    gallery_ids = []
    for element in elements:
        if element['media'].startswith('[gallery'):
            gallery_ids_match = re.search(r'ids="([\d,]+)"', element['media'])
            if gallery_ids_match:
                gallery_ids.extend(gallery_ids_match.group(1).split(','))

    wp_posts = WpPosts.objects.filter(post_type="attachment", id__in=gallery_ids)
    wp_posts_dict = {str(post.id): post.guid for post in wp_posts}

    updated_elements = []
    for element in elements:
        if element['media'].startswith('[gallery'):
            gallery_ids_match = re.search(r'ids="([\d,]+)"', element['media'])
            if gallery_ids_match:
                ids = gallery_ids_match.group(1).split(',')
                links = [wp_posts_dict.get(id, '') for id in ids]
                element['media'] = f'[gallery link="file" ids="{",".join(links)}"]'
        updated_elements.append(element)
    return updated_elements

def preprocess_article(article):
    post_content = article['post_content']
    post_id = article['id']
    post_date = article['post_date']
    post_title = article['post_title']

    soup = BeautifulSoup(post_content, "html.parser")
    structured_data = extract_elements(soup.body if soup.body else soup)

    final_elements = []
    for element in structured_data:
        if '[gallery' in element.get('text', ''):
            final_elements.extend(handle_galleries(element['text']))
        else:
            final_elements.append(element)

    final_elements = replace_gallery_ids_with_links(final_elements)

    output_data = {
        "post_date": post_date,
        "post_content": post_content,
        "post_title": post_title,
        "post_id": post_id,
        "content": final_elements
    }

    return output_data
