import unittest
from unittest.mock import patch, Mock
from .preprocessing import preprocess_article
from .tasks import fetch_and_process_post

class TestPostContentProcessing(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.sample_post = {
            'id': 1,
            'post_type': 'post',
            'post_title': 'Test Title',
            'post_content': '''
                first<a href="https://arabgt.com/" target="_blank" rel="noopener"><strong>link</strong></a>second
                <p>هذه هي أجدد سيارات بورش \t2024.</p>
                <h2>نظرة عامة</h2>
                https://www.youtube.com/watch?v=FTfuQyc7IEw
                <strong>قد يهمك هذه آخر تغطيات عرب جي تي مع سيارات جديدة :</strong>
                <p><img src="https://example.com/porsche.jpg" /></p>
                <p>hello world<img src="https://example.com/porsche.jpg" />End</p>
                <iframe title="YouTube video player" src="//www.youtube.com/embed/sK6dEN73n0E?si=jNOsU0mt3ogEjA6p" width="850" height="478" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
                [gallery link="file" ids="354716,354713"]
                <p>click <a href="https://www.google.com">here</a> to continue</p>
                <p><a href="www.link.com">paragraph with a link</a></p>
                <h1><a href="www.link.com">paragraph with a link</a></h1>
                <h1>click <a href="https://www.google.com">here</a> to continue</h1>
                <ul><li>one</li><li>two</li><li>three</li></ul>
                <ul><li>one <a href="www.audteye.com">link</a></li><li>two</li><li>three</li></ul>
            ''',
            'post_date': '2024-01-01',
            'post_modified': '2024-01-01',
            'post_author': 1
        }

    @patch('news.models.WpPosts.objects.filter')
    @patch('api.models.Post.objects.create')
    @patch('api.models.Post.objects.update_or_create')
    def test_process_post_content(self, mock_update_or_create, mock_create, mock_wp_posts_filter):
        # Mocking the response for gallery images
        mock_wp_posts_filter.return_value = [
            Mock(id='354716', guid='https://arabgt.com/wp-content/uploads/2023/12/بورش-باناميرا-2024-1-1.jpg'),
            Mock(id='354713', guid='https://arabgt.com/wp-content/uploads/2023/12/باناميرا-الجديدة-.jpg')
        ]

        mock_create.return_value = Mock(id=1)
        mock_update_or_create.return_value = (Mock(id=1), True)

        fetch_and_process_post(self.sample_post, override_existing=False)

        mock_create.assert_called_once()
        created_post = mock_create.call_args[1]

        expected_content = [
            {
                "text": "",
                "heading": "",
                "media": {},
                "type": "rich",
                "data": [
                    {"text": "first", "heading": "", "media": {}},
                    {"text": "link", "url": "https://arabgt.com/", "heading": "", "media": {}},
                    {"text": "second", "heading": "", "media": {}}
                ]
            },
            {'text': 'هذه هي أجدد سيارات بورش 2024.', 'media': {}, 'heading': ''},
            {'text': '', 'media': {}, 'heading': 'نظرة عامة'},
            {'text': '', 'media': {'youtube': 'https://www.youtube.com/watch?v=FTfuQyc7IEw'}, 'heading': ''},
            {'text': '', 'media': {}, 'heading': 'قد يهمك هذه آخر تغطيات عرب جي تي مع سيارات جديدة :'},
            {'text': '', 'media': {'image': 'https://example.com/porsche.jpg'}, 'heading': ''},
            {'text': 'hello world', 'media': {}, 'heading': ''},
            {'text': '', 'media': {'image': 'https://example.com/porsche.jpg'}, 'heading': ''},
            {'text': 'End', 'media': {}, 'heading': ''},
            {'text': '', 'media': {'youtube': 'https://www.youtube.com/watch?v=sK6dEN73n0E'}, 'heading': ''},
            {'text': '', 'media': {'gallery': [
                'https://arabgt.com/wp-content/uploads/2023/12/بورش-باناميرا-2024-1-1.jpg',
                'https://arabgt.com/wp-content/uploads/2023/12/باناميرا-الجديدة-.jpg'
            ]}, 'heading': ''},
            {
                "text": "",
                "heading": "",
                "media": {},
                "type": "rich",
                "data": [
                    {"text": "click", "heading": "", "media": {}},
                    {"text": "here", "url": "https://www.google.com", "heading": "", "media": {}},
                    {"text": "to continue", "heading": "", "media": {}}
                ]
            },
            {"text": "paragraph with a link", "url": "www.link.com", "heading": "", "media": {}},
            {"text": "", "url": "www.link.com", "heading": "paragraph with a link", "media": {}},
            {
                "text": "",
                "heading": "",
                "media": {},
                "type": "rich_heading",
                "data": [
                    {"text": "click", "heading": "", "media": {}},
                    {"text": "here", "url": "https://www.google.com", "heading": "", "media": {}},
                    {"text": "to continue", "heading": "", "media": {}}
                ]
            },
            {"text": "• one\n• two\n• three", "heading": "", "media": {}},
            {
                "text": "",
                "heading": "",
                "media": {},
                "type": "rich",
                "data": [
                    {"text": "• one", "heading": "", "media": {}},
                    {"text": "link\n", "url": "www.audteye.com", "heading": "", "media": {}},
                    {"text": "• two\n• three", "heading": "", "media": {}}
                ]
            },
            {'external_links': ['https://www.google.com', 'www.link.com']}
        ]
        
        # Compare the actual content with expected content
        self.assertEqual(created_post['content'], expected_content)
