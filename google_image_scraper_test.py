import unittest
from unittest.mock import patch, Mock
from google_image_scraper import resize_image
from PIL import Image
import io
import os
import logging


class GoogleImageScraperTest(unittest.TestCase):

    @patch('builtins.open', new_callable=Mock)
    @patch('PIL.Image.open')
    @patch('io.BytesIO')
    def test_resize_image_success(self, mock_bytesio, mock_image_open, mock_builtin_open):
        # setup mocks
        mock_image = Mock(spec=Image.Image)
        mock_image_open.return_value = mock_image
        mock_output = Mock()
        mock_bytesio.return_value = mock_output
        folder_name = 'images_test'
        filename = 'test.jpg'
        file_path = os.path.join(folder_name, filename)
        # call function
        result = resize_image(file_path)

        # assert
        mock_image_open.assert_called_once_with(file_path)
        mock_image.thumbnail.assert_called_once_with((120, 120))
        mock_image.save.assert_called_once_with(mock_output, format='JPEG')
        self.assertEqual(result, mock_output.getvalue())
