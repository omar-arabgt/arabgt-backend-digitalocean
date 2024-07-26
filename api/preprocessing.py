import re
from bs4 import BeautifulSoup
from news.models import WpPosts, WpPostmeta
from .models import Post
from django.db.models import Q
import urllib.parse

def extract_elements(element):
    """
    Extracts structured elements from HTML content.

    Input:
    - element: A BeautifulSoup element representing the HTML content to be parsed.

    Functionality:
    - Parses the HTML content to extract text, headings, media elements (such as images, iframes, YouTube videos), and external links.
    - Processes various HTML tags (<strong>, <a>, <h1> to <h6>, <ul>, <ol>, <iframe>, and <img>) to structure the content into elements.

    Output:
    - Returns a tuple:
      - elements: A list of dictionaries representing structured content elements.
      - external_links: A list of external links found in the content.
    """
    elements = []
    text_buffer = []
    external_links = []

    def add_text_buffer_to_elements():
        if text_buffer:
            text = ''.join(text_buffer).strip()
            if text:
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
                    text_buffer.append(child.get_text())
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
                for li in child.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        external_links.append(a_tag['href'])
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
    elements = [element for element in elements if element['text'] or element['media'] or element['heading']]
    return elements, external_links

def handle_galleries(text):
    """
    Handles gallery shortcodes in the text.

    Input:
    - text: A string containing the post content with possible gallery shortcodes.

    Functionality:
    - Splits the text by gallery shortcodes.
    - Extracts gallery IDs from the shortcodes and creates elements for them.

    Output:
    - Returns a list of elements with gallery information replaced.
    """
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
    """
    Replaces gallery IDs with actual image URLs.

    Input:
    - elements: A list of elements containing gallery IDs.

    Functionality:
    - Fetches image URLs for the given gallery IDs from the database.
    - Replaces gallery IDs with the corresponding image URLs.

    Output:
    - Returns an updated list of elements with image URLs.
    """
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
    """
    Retrieves the thumbnail URL for a given post.

    Input:
    - post_id: An integer representing the ID of the post.

    Functionality:
    - Fetches the thumbnail ID from the post metadata.
    - Retrieves the corresponding thumbnail URL.

    Output:
    - Returns the thumbnail URL as a string.
    """
    thumbnail_id = WpPostmeta.objects.filter(post_id=post_id, meta_key='_thumbnail_id').values_list('meta_value', flat=True).first()
    thumbnail_url = None
    if thumbnail_id:
        thumbnail_url = WpPostmeta.objects.filter(post_id=thumbnail_id, meta_key='_wp_attached_file').values_list('meta_value', flat=True).first()
    
    return thumbnail_url

def process_external_links(external_links):
    """
    Processes external links to categorize them.

    Input:
    - external_links: A list of external links found in the content.

    Functionality:
    - Categorizes links that belong to 'arabgt.com' as related articles.
    - Cleans and separates other external links.

    Output:
    - Returns a tuple:
      - related_articles: A list of related article links.
      - cleaned_external_links: A list of cleaned external links.
    """
    related_articles = []
    cleaned_external_links = []
    
    for link in external_links:
        if "arabgt.com" in link:
            decoded_link = urllib.parse.unquote(link)
            parts = decoded_link.split('/')
            if len(parts) > 0:
                related_articles.append(decoded_link)
        else:
            cleaned_external_links.append(link)
    
    return related_articles, cleaned_external_links

def normalize_title(title):
    """
    Normalizes a given title string.

    Input:
    - title: A string representing the title to be normalized.

    Functionality:
    - Converts the title to lowercase.
    - Replaces dashes and other special characters with spaces.
    - Removes non-alphanumeric characters.
    - Trims extra whitespace.

    Output:
    - Returns the normalized title as a string.
    """
    title = title.lower()
    title = re.sub(r'[\-\–]', ' ', title)
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def update_related_article_ids(post):
    """
    Updates related article IDs based on links in the content.

    Input:
    - post: A Post object representing the current post.

    Functionality:
    - Extracts titles from related article links.
    - Normalizes the titles and searches for matching posts in the database.
    - Updates related article links with the corresponding post IDs.

    Output:
    - Returns a tuple:
      - post: The updated Post object.
      - missing_titles: A list of missing titles and corresponding post IDs.
    """
    updated = False
    missing_titles = []
    related_articles_in_content = post.related_articles.copy()
    for index, related_article_link in enumerate(related_articles_in_content):
        if related_article_link.isdigit():
            continue
        try:
            title = related_article_link.split('/')[-2].replace('-', ' ')
        except IndexError:
            missing_titles.append({"title": "Invalid URL", "id": post.id})
            continue
        normalized_title = normalize_title(title)
        words = normalized_title.split()
        query = Q()
        for word in words:
            query &= Q(title__icontains=word)
        related_post = Post.objects.filter(query).first()
        if related_post:
            related_articles_in_content[index] = str(related_post.id)
            updated = True
        else:
            missing_titles.append({"title": title, "id": post.id})

    if updated:
        post.related_articles = related_articles_in_content
        post.save()

    return post, missing_titles

def preprocess_article(article):
    """
    Preprocesses an article to extract and structure its content.

    Input:
    - article: A dictionary containing the article data with keys 'post_content', 'id', 'post_date', and 'post_title'.

    Functionality:
    - Parses the article content using BeautifulSoup.
    - Extracts structured data and external links from the content.
    - Handles gallery shortcodes and replaces them with actual image URLs.
    - Processes external links to separate related articles.
    - Retrieves the thumbnail URL for the article.

    Output:
    - Returns a dictionary containing:
      - post_date: The date of the post.
      - post_content: The original content of the post.
      - post_title: The title of the post.
      - post_id: The ID of the post.
      - thumbnail: The thumbnail URL of the post.
      - content: A list of structured content elements.
      - related_articles: A list of related article links.
    """
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

    if cleaned_external_links:
        final_elements.append({
            "external_links": cleaned_external_links
        })
        
    thumbnail_url = get_thumbnail(post_id)
    thumbnail_url_with_base = f'https://arabgt.com/wp-content/uploads/{thumbnail_url}'

    output_data = {
        "post_date": post_date,
        "post_content": post_content,
        "post_title": post_title,
        "post_id": post_id,
        "thumbnail": thumbnail_url_with_base,
        "content": final_elements,
        "related_articles": related_articles
    }
    
    return output_data
