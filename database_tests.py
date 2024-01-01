from unittest import TestCase, mock
from unittest.mock import patch, Mock, MagicMock
from database import insert_image, create_images_table
import psycopg2


class DatabaseTests(TestCase):

    @patch('database.create_connection')
    def test_create_images_table(self, mock_create_connection):
        # setup mocks
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = (mock_connection, mock_cursor)

        # call function
        create_images_table()

        # assertions
        mock_create_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "create table if not exists images(id serial primary key,image bytea)"
        )

    @patch('database.create_connection')
    def test_insert_image_to_db(self, mock_create_connection):
        # setup mocks
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = (mock_connection, mock_cursor)

        # call function
        fake_image = b'\x01\x02\x03\x04\x05'
        insert_image(fake_image)

        query = f'INSERT INTO images (image) VALUES({psycopg2.Binary(fake_image)})'

        # assertions
        mock_create_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
