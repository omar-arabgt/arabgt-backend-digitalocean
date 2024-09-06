import unittest
from unittest.mock import patch, Mock
from .preprocessing import preprocess_article
from .tasks import fetch_and_process_post

class TestPostContentProcessing(unittest.TestCase):

    def setUp(self):
        self.sample_post = {
            'id': 1,
            'post_type': 'post',
            'post_title': 'Test Title',
            'post_content': '''
                <p>هذه هي أجدد سيارات بورش 2024.</p>
                <h2>نظرة عامة</h2>
                https://www.youtube.com/watch?v=FTfuQyc7IEw
                <strong>قد يهمك هذه آخر تغطيات عرب جي تي مع سيارات جديدة :</strong>
                <p><img src="https://example.com/porsche.jpg" /></p>
                <iframe title="YouTube video player" src="//www.youtube.com/embed/sK6dEN73n0E?si=jNOsU0mt3ogEjA6p" width="850" height="478" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
                [gallery link="file" ids="354716,354713"]
            ''',
            'post_date': '2024-01-01',
            'post_modified': '2024-01-01',
            'post_author': 1
        }

    @patch('api.models.Post.objects.create')
    @patch('api.models.Post.objects.update_or_create')
    def test_process_post_content(self, mock_update_or_create, mock_create):
        mock_create.return_value = Mock(id=1)
        mock_update_or_create.return_value = (Mock(id=1), True)

        fetch_and_process_post(self.sample_post, override_existing=False)

        mock_create.assert_called_once()
        created_post = mock_create.call_args[1]

        expected_content = [
            {'text': 'هذه هي أجدد سيارات بورش 2024.', 'media': {}, 'heading': ''},
            {'text': '', 'media': {}, 'heading': 'نظرة عامة'},
            {'text': '', 'media': {'youtube': 'https://www.youtube.com/watch?v=FTfuQyc7IEw'}, 'heading': ''},
            {'text': '', 'media': {}, 'heading': 'قد يهمك هذه آخر تغطيات عرب جي تي مع سيارات جديدة :'},
            {'text': '', 'media': {'image': 'https://example.com/porsche.jpg'}, 'heading': ''},
            {'text': '', 'media': {'youtube': 'https://www.youtube.com/watch?v=sK6dEN73n0E'}, 'heading': ''},
            {'text': '', 'media': {'gallery': [
                'https://arabgt.com/wp-content/uploads/2023/12/بورش-باناميرا-2024-1-1.jpg',
                'https://arabgt.com/wp-content/uploads/2023/12/باناميرا-الجديدة-.jpg'
            ]}, 'heading': ''}
        ]

        # Compare the actual content with expected content
        self.assertEqual(created_post['content'], expected_content)
