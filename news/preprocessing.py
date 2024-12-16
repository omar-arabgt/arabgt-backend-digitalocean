import re
import json
import urllib.parse
from bs4 import BeautifulSoup

from django.db.models import Q

from api.models import Post
from .models import WpPosts, WpPostmeta

from urllib.parse import urlparse, unquote

# def replace_url(url):
#     # Decode the URL
#     clean_url = re.search(r'https?://[^\s"]+', url).group()

#     decoded_url = unquote(clean_url)
#     parsed_url = urlparse(decoded_url)
#     title =  parsed_url.path.strip('/').split('/')[-1].replace('-', ' ').lower()
#     post_instance = Post.objects.filter(normalized_title__icontains=title).first()
#     return f'https://localhost/api/posts/{post_instance.id}'

import re
from urllib.parse import unquote, urlparse

def replace_url(url):
    # Check if URL is from arabgt.com

    # Decode the URL
    clean_url = re.search(r'https?://[^\s"]+', url).group()
    if not clean_url.startswith("https://arabgt.com/"):
        return clean_url

    decoded_url = unquote(clean_url)
    parsed_url = urlparse(decoded_url)
    # Split the path into parts
    path_parts = parsed_url.path.strip('/').split('/')

    # Special case for 'news-tags'
    if "news-tags" in path_parts:
        # Find the index of 'news-tags' and get the part after it
        news_tag_index = path_parts.index("news-tags")
        if news_tag_index + 1 < len(path_parts):
            tag_part = path_parts[news_tag_index + 1]
            # Replace hyphens with spaces
            formatted_tag = tag_part.replace('-', ' ')
            return f"/api/posts/?tag={formatted_tag}"

    # # Define allowed tags
    # tags = {
    #     "اخبار-سيارات",
    #     "سيارات-معدلة",
    #     # Add your other 26 tags here
    # }

    # # Check if the URL contains any of the allowed tags
    # if not any(tag in path_parts for tag in tags):
    #     return None

    # Extract the title part of the URL
    title = normalize_title(path_parts[-1]) 
    # Find the first matching Post instance
    post_instance = Post.objects.filter(normalized_title__icontains=title).first()
    # Return the local API URL if a post is found, else return None
    if post_instance:
        return f'/api/posts/{post_instance.id}'
    else:
        print(f'arabgt {url}')
        return clean_url

# 365716

def process_list_item_with_regex(html):
    """
    Processes <ul> or <ol> elements to extract bullet points with and without links.
    Returns structured content, treating lists with links as 'rich' and lists without links as plain text.
    """
    soup = BeautifulSoup(html, 'html.parser')
    list_items = soup.find_all('li')

    rich_data = []
    has_link = False

    for idx, item in enumerate(list_items):
        item_rich_data = []
        bullet_added = False

        for content in item.contents:
            if isinstance(content, str):
                text = content.strip()
                if text:
                    if not bullet_added:
                        text = '• ' + text
                        bullet_added = True
                    else:
                        text = ' ' + text 
                    item_rich_data.append({
                        "text": text,
                        "heading": "",
                        "media": {}
                    })
            elif content.name == 'a':
                has_link = True
                link_text = content.get_text(strip=True)
                link_url = content.get('href', '')
                if not bullet_added:
                    link_text = '• ' + link_text
                    bullet_added = True
                else:
                    link_text = ' ' + link_text 
                item_rich_data.append({
                    "text": link_text,
                    "url": replace_url(link_url),
                    "heading": "",
                    "media": {}
                })
            else:
                pass

        if idx < len(list_items) - 1:
            if item_rich_data:
                last_text = item_rich_data[-1]['text']
                item_rich_data[-1]['text'] = last_text + '\n'

        rich_data.extend(item_rich_data)

    if not has_link:
        merged_bullet_points = "".join([item['text'] for item in rich_data])
        return [{
            "text": merged_bullet_points,
            "heading": "",
            "media": {}
        }]

    result = [{
        "text": "",
        "heading": "",
        "media": {},
        "type": "rich",
        "data": rich_data
    }]

    return result

def extract_elements(element):
    """
    Extract structured elements from HTML content recursively.
    Returns a list of content elements with text, media, and headings.
    """
    elements = []
    external_links = set()
    accumilated_rich = []

    youtube_pattern = re.compile(r'https?://(www\.)?(youtube\.com|youtu\.be)/[^\s]+')

    def add_element(text='', media=None, heading='', url=None, type=None, rich_data=None):
        if text.strip() or media or heading.strip() or rich_data:
            text = text.strip() if text else ''
            if text and youtube_pattern.match(text):
                media = media or {}
                media['youtube'] = text
                text = ''
            element = {
                'text': text,
                'media': media or {},
                'heading': heading.strip() if heading else ''
            }
            if url:
                element['url'] = url
            if type == 'rich' or type == 'rich_heading':
                element['type'] = type
                element['data'] = rich_data
            elements.append(element)

    for child in element.children:
        if isinstance(child, str):
            text = child.strip()
            if text:
                accumilated_rich.append({"text": text, "heading": "", "media": {}})
        elif child.name == 'a' and child.parent.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            url = child.get('href', '')
            link_text = child.get_text(strip=True)
            external_links.add(url)
            if(not url.startswith("https://arabgt.com/wp-content")):
              accumilated_rich.append({"text": link_text, "url": replace_url(url), "heading": "", "media": {}})
              external_links.add(url)
            else:
              if link_text.strip():
                  add_element(text=link_text.strip())
                  link_text = ""
              add_element(media={"image": replace_url(url)})
        else:
            if accumilated_rich:
                has_link = any('url' in item for item in accumilated_rich)
                if has_link:
                    add_element(type='rich', rich_data=accumilated_rich.copy())
                else:
                    for item in accumilated_rich:
                        add_element(text=item['text'])
                accumilated_rich.clear()

            if child.name in ['ul', 'ol']:
                list_elements = process_list_item_with_regex(str(child))
                if list_elements:
                    elements.extend(list_elements)

            elif child.name == 'p':
                rich_data = []
                paragraph_text = ""
                for p_child in child.children:
                    if isinstance(p_child, str):
                        paragraph_text += p_child.strip() + " "
                    elif p_child.name == 'a':
                        url = p_child.get('href', '')
                        if paragraph_text.strip():
                            rich_data.append({"text": paragraph_text.strip(), "heading": "", "media": {}})
                            paragraph_text = ""
                        if(not url.startswith("https://arabgt.com/wp-content")):
                          rich_data.append({"text": p_child.get_text(strip=True), "url": replace_url(url), "heading": "", "media": {}})
                          external_links.add(url)
                        else:
                          if p_child.get_text(strip=True):
                              add_element(text=p_child.get_text(strip=True))
                              link_text = ""
                          add_element(media={"image": replace_url(url)})
                        
                    elif p_child.name == 'img':
                        if paragraph_text.strip():
                            add_element(text=paragraph_text.strip())
                            paragraph_text = ""
                        add_element(media={"image": p_child.get('src', '')})

                if paragraph_text.strip():
                    rich_data.append({"text": paragraph_text.strip(), "heading": "", "media": {}})

                if len(rich_data) > 1:
                    add_element(type='rich', rich_data=rich_data)
                elif len(rich_data) == 1:
                    if 'url' in rich_data[0]:
                        add_element(text=rich_data[0]['text'], url=rich_data[0]['url'])
                    else:
                        add_element(text=rich_data[0]['text'])

            elif child.name == 'a':
                href = child.get('href', '')
                external_links.add(href)
                if child.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    add_element(heading=child.get_text(strip=True), url=href)
                else:
                    add_element(text=child.get_text(strip=True), url=href)

            elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                heading_rich_data = []
                heading_text = ""
                for h_child in child.children:
                    if isinstance(h_child, str):
                        heading_text += h_child.strip() + " "
                    elif h_child.name == 'a':
                        url = h_child.get('href', '')
                        if heading_text.strip():
                            heading_rich_data.append({"text": heading_text.strip(), "heading": "", "media": {}})
                            heading_text = ""
                        if(not url.startswith("https://arabgt.com/wp-content")):
                          heading_rich_data.append({"text": h_child.get_text(strip=True), "url": replace_url(url), "heading": "", "media": {}})
                          external_links.add(url)
                        else:
                          if h_child.get_text(strip=True):
                              add_element(text=h_child.get_text(strip=True))
                              link_text = ""
                          add_element(media={"image": replace_url(url)})

                if heading_text.strip():
                    heading_rich_data.append({"text": heading_text.strip(), "heading": "", "media": {}})

                if len(heading_rich_data) > 1:
                    add_element(type='rich_heading', rich_data=heading_rich_data)
                elif len(heading_rich_data) == 1:
                    add_element(heading=heading_rich_data[0]['text'], url=heading_rich_data[0].get('url', None))
                else:
                    add_element(heading=child.get_text(strip=True))

            elif child.name == 'strong':
                if not accumilated_rich:
                    add_element(heading=child.get_text(strip=True))
                else:
                    accumilated_rich.append({"text": child.get_text(strip=True), "heading": "", "media": {}})

            elif child.name == 'iframe':
                src = child.get('src', '')
                if 'youtube' in src:
                    youtube_id_match = re.search(r"embed/([^?]+)", src)
                    if youtube_id_match:
                        youtube_id = youtube_id_match.group(1)
                        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
                        add_element(media={"youtube": youtube_url})
                else:
                    add_element(media={"iframe": src})

            elif child.name == 'img':
                src = child.get('src', '')
                add_element(media={"image": src})

            elif '[gallery' in str(child):
                gallery_elements = handle_galleries(str(child))
                elements.extend(gallery_elements)

            else:
                nested_elements, nested_links = extract_elements(child)
                elements.extend(nested_elements)
                external_links.update(nested_links)

    if accumilated_rich:
        has_link = any('url' in item for item in accumilated_rich)
        if has_link:
            add_element(type='rich', rich_data=accumilated_rich.copy())
        else:
            for item in accumilated_rich:
                add_element(text=item['text'])
        accumilated_rich.clear()

    return elements, list(external_links)



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
    - Recursively processes nested elements, including within 'rich' and 'rich_heading' elements.

    Output:
    - Returns an updated list of elements with image URLs.
    """
    gallery_ids = []

    # Function to collect all gallery IDs from elements and nested data
    def collect_gallery_ids(element):
        if 'media' in element and 'gallery' in element['media']:
            gallery_ids.extend(element['media']['gallery'])
        if element.get('type') in ['rich', 'rich_heading']:
            for item in element['data']:
                collect_gallery_ids(item)

    # Collect gallery IDs from all elements
    for element in elements:
        collect_gallery_ids(element)

    # Fetch image URLs from the database
    wp_posts = WpPosts.objects.filter(post_type="attachment", id__in=gallery_ids)
    wp_posts_dict = {str(post.id): post.guid for post in wp_posts}

    # Function to replace gallery IDs with URLs in elements and nested data
    def replace_ids_in_element(element):
        if 'media' in element and 'gallery' in element['media']:
            ids = element['media']['gallery']
            # Replace IDs with URLs, defaulting to an empty string if not found
            links = [wp_posts_dict.get(id.strip(), '') for id in ids]
            element['media']['gallery'] = links
        if element.get('type') in ['rich', 'rich_heading']:
            for item in element['data']:
                replace_ids_in_element(item)

    # Replace gallery IDs with URLs in all elements
    for element in elements:
        replace_ids_in_element(element)
    
    return elements

def clean_instagram_references(elements):
    filtered = []
    
    for item in elements:
        text_val = item.get('text', '').strip()
        has_instagram_text = "View this post on Instagram" in text_val
        has_shared_by_text = "A post shared by" in text_val

        has_url = 'url' in item
        has_media = item.get('media', {})
        has_heading = item.get('heading', '').strip()
        has_external_links = 'external_links' in item

        has_other_data = has_url or has_media or has_heading or has_external_links

        if text_val == "View this post on Instagram" and not has_other_data:
            continue
        elif has_instagram_text or has_shared_by_text:
            if has_other_data:
                item['text'] = ""
                filtered.append(item)
            else:
                continue
        else:
            filtered.append(item)

    return filtered



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


def get_related_article_ids(related_articles):
    """
    Get post IDs from related article links in the content.

    Input:
    - related_articles: A list of related article links

    Functionality:
    - Extracts titles from related article links.
    - Normalizes the titles and searches for matching posts in the database.

    Output:
    - Returns a list of corresponding post IDs:
    """
    result = []
    for related_article_link in related_articles.copy():
        if related_article_link.isdigit():
            continue
        try:
            title = related_article_link.split('/')[-2].replace('-', ' ')
        except IndexError:
            continue

        normalized_title = normalize_title(title)
        words = normalized_title.split()
        query = Q()
        for word in words:
            query &= Q(title__icontains=word)
        related_post = Post.objects.filter(query).first()
        if related_post:
            result.append(related_post.id)

    return result


def process_galleries_in_element(element):
    if element.get('type') in ['rich', 'rich_heading']:
        new_data = []
        for item in element['data']:
            processed_items = process_galleries_in_element(item)
            new_data.extend(processed_items)
        element['data'] = new_data
        return [element]
    else:
        if '[gallery' in element.get('text', ''):
          return handle_galleries(element['text'])
        else:
            return [element]


def preprocess_captions_and_galleries(text):
    """
    Replaces [caption] and [gallery] shortcodes with HTML tags for easier parsing.
    """
    caption_pattern_start = r'\[caption[^\]]*\]'
    caption_pattern_end = r'\[/caption\]'

    text = re.sub(caption_pattern_start, '', text)
    text = re.sub(caption_pattern_end, '', text)

    return text


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
    post_content = post_content.replace('\t', '')
    post_id = article['id']

    post_content = preprocess_captions_and_galleries(post_content)

    soup = BeautifulSoup(post_content, "html.parser")
    structured_data, external_links = extract_elements(soup.body if soup.body else soup)
    # print("Structured Data:", structured_data)

    final_elements = []
    
    for element in structured_data:
        processed_elements = process_galleries_in_element(element)
        final_elements.extend(processed_elements)


    final_elements = replace_gallery_ids_with_links(final_elements)
    final_elements = clean_instagram_references(final_elements)
    
    related_articles, cleaned_external_links = process_external_links(external_links)

    if cleaned_external_links:
        final_elements.append({
            "external_links": cleaned_external_links
        })

    thumbnail_url = get_thumbnail(post_id)
    thumbnail_url_with_base = f'https://arabgt.com/wp-content/uploads/{thumbnail_url}' if thumbnail_url else None

    output_data = {
        "thumbnail": thumbnail_url_with_base,
        "content": final_elements,
        "related_articles": related_articles
    }
    
    return output_data

def preprocess_video_article(article):
    post_content = article['post_content']
    post_id = article['id']
    
    youtube_pattern = re.compile(r'https?://(www\.)?(youtube\.com|youtu\.be)/[^\s]+')
    facebook_pattern = re.compile(r'<iframe[^>]+src="https?://www\.facebook\.com/plugins/video\.php[^"]+"[^>]*></iframe>')
    twitter_pattern = re.compile(r'<blockquote class="twitter-tweet".*?</blockquote>', re.DOTALL)
    twitter_media_pattern = re.compile(r'<a href="(https?://(?:t\.co|pic\.twitter\.com|pic\.x\.com)/[^"]+)"')
    instagram_pattern = re.compile(r'<blockquote class="instagram-media".*?</blockquote>', re.DOTALL)
    instagram_permalink_pattern = re.compile(r'data-instgrm-permalink="([^"]+)"')

    media_content = None
    
    
    youtube_match = youtube_pattern.search(post_content)
    if youtube_match:
        media_content = youtube_match.group(0)
        post_content = youtube_pattern.sub('', post_content)

    
    facebook_match = facebook_pattern.search(post_content)
    if facebook_match:
        media_content = facebook_match.group(0)
        post_content = facebook_pattern.sub('', post_content)

    
    twitter_match = twitter_pattern.search(post_content)
    if twitter_match:
        tweet_content = twitter_match.group(0)
        media_match = twitter_media_pattern.search(tweet_content)
        if media_match:
            media_content = media_match.group(1)
        post_content = twitter_pattern.sub('', post_content)

    
    instagram_match = instagram_pattern.search(post_content)
    if instagram_match:
        instagram_content = instagram_match.group(0)
        permalink_match = instagram_permalink_pattern.search(instagram_content)
        if permalink_match:
            media_content = permalink_match.group(1)
        post_content = instagram_pattern.sub('', post_content)

    
    soup = BeautifulSoup(post_content, "html.parser")
    
    
    for script in soup(["script", "style"]):
        script.decompose()

    text_content = soup.get_text(separator=" ").strip()

    
    text_content = text_content.replace('\xa0', ' ')

    content = {
        "text": text_content,
        "media": {}
    }

    if youtube_match:
        content["media"]["youtube"] = media_content
    else:
        content["media"]["iframe"] = media_content

    thumbnail_url = get_thumbnail(post_id)
    thumbnail_url_with_base = f'https://arabgt.com/wp-content/uploads/{thumbnail_url}' if thumbnail_url else None

    output_data = {
        "thumbnail": thumbnail_url_with_base,
        "content": [content],
    }

    return output_data
