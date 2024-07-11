import re
from bs4 import BeautifulSoup
from news.models import WpPosts, WpPostmeta

def extract_elements(element):
    elements = []
    text_buffer = []

    def add_text_buffer_to_elements():
        if text_buffer:
            text = ' '.join(text_buffer).strip()
            if text:  # Only add if the text is not empty
                elements.append({
                    "text": text,
                    "media": {},
                    "heading": ""
                })
            text_buffer.clear()

    for child in element.children:
        if isinstance(child, str):
            text_buffer.append(child.strip())
        else:
            tag_name = child.name
            attributes = child.attrs
            text = child.get_text(strip=True)

            if tag_name == 'strong' and (not child.previous_sibling or not child.next_sibling):
                add_text_buffer_to_elements()
                elements.append({
                    "text": "",
                    "media": {},
                    "heading": text
                })
            elif tag_name == 'a':
                text_buffer.append(text)
            elif tag_name == 'strong':
                if (child.previous_sibling and '\n' in child.previous_sibling) or (child.next_sibling and '\n' in child.next_sibling):
                    add_text_buffer_to_elements()
                    elements.append({
                        "media": {},
                        "heading": text,
                        "text": "",
                    })
                else:
                    text_buffer.append(text)
            else:
                add_text_buffer_to_elements()
                if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    elements.append({
                        "text": "",
                        "media": {},
                        "heading": text
                    })
                elif tag_name == 'strong':
                    elements.append({
                        "text": text,
                        "media": {},
                        "heading": "",
                        "bold": True
                    })
                elif tag_name in ['ul', 'ol']:
                    bullets = "\n".join([f"• {li.get_text(strip=True)}" for li in child.find_all('li')])
                    elements.append({
                        "text": bullets,
                        "media": {},
                        "heading": ""
                    })
                elif tag_name == 'iframe':
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
                    src = attributes.get('src', '')
                    elements.append({
                        "text": "",
                        "media": {"image": src},
                        "heading": ""
                    })
                else:
                    elements.append({
                        "text": text,
                        "media": {},
                        "heading": ""
                    })

    add_text_buffer_to_elements()

    # Remove any empty dictionary items
    elements = [element for element in elements if element['text'] or element['media'] or element['heading']]

    return elements

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
