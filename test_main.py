import unittest
import re
import os
import tempfile as tf
from unittest.mock import MagicMock, patch, mock_open

from main import get_id, get_files

@unittest.skip("already tested")
class TestGetId(unittest.TestCase):

    def test_empty_url(self):
        self.assertIsNone(get_id(''))
    
    def test_simple_url(self):
        self.assertEqual(get_id('https://m.youtube.com/watch?v=SA2iWivDJiE'), 'SA2iWivDJiE')
 
    def test_simple_param_url(self):
        self.assertEqual(get_id('https://m.youtube.com/watch?v=SA2iWivDJiE&t=1m3s'), 'SA2iWivDJiE')

    def test_long_param_url(self):
        self.assertEqual(get_id('https://www.youtube.com/watch?v=SA2iWivDJiE&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6'),'SA2iWivDJiE')

    def test_share_url(self):
        self.assertEqual(get_id('https://www.youtube.com/watch?v=SA2iWivDJiE&list=n0g-Y0oo5Qs'), 'SA2iWivDJiE')

    def test_shortened_url(self):
        self.assertEqual(get_id('https://youtu.be/SA2iWivDJiE'), 'SA2iWivDJiE')

    def test_shortened_param_url(self):
        self.assertEqual(get_id('https://youtu.be/SA2iWivDJiE&t=1m3s'), 'SA2iWivDJiE')

    def test_embed_url(self):
        self.assertEqual(get_id('https://m.youtube.com/embed/SA2iWivDJiE'), 'SA2iWivDJiE')
    def test_embed_param_url(self):
        self.assertEqual(get_id('https://m.youtube.com/embed/SA2iWivDJiE&t=1m3s'), 'SA2iWivDJiE')

@unittest.skip
class TestGetFiles(unittest.TestCase):
    def setUp(self):
        pass 
    def test_get_files_no_match(self):
        with patch('main.glob') as mocked_glob:
            mocked_glob.return_value = []
            result = get_files('url_extract_*.json')
            self.assertEqual(result, [])
            mocked_glob.assert_called_with('url_extract_*.json')

    def test_get_matched(self):
        with patch('main.glob') as mocked_glob:
            mocked_glob.return_value = ['url_extract_1.json', 'url_extract_2.json']
            result = get_files()
            self.assertEqual(result, ['url_extract_1.json', 'url_extract_2.json'])
            mocked_glob.assert_called_with('url_extract_*.json')

    def test_read_channels_line_by_line(self):
        with patch('builtins.open', mock_open(read_data='line1\nline2\nline3')):
            func_result = self.obj.channel_list()
            expected_result = ['line1', 'line2', 'line3']
            self.assertEqual(sorted(expected_result), sorted(func_result))

    def test_read_channels_empty_line(self):
        '''should exit when channel list is empty'''
        with patch('builtins.open', mock_open(read_data='')):
             with self.assertRaises(SystemExit):
                self.obj.channel_list()

    @unittest.skip # to implement this checking later
    def test_read_channels_empty_line_bw_channel_list(self):
        '''should warn with line number that url is wrong'''
        with patch('builtins.open', mock_open(read_data='line1\nline2\n""')):
            with self.assertRaises(EmptyLine):
                self.obj.channel_list()

    def test_get_files_no_match(self):
        with tf.NamedTemporaryFile(prefix='url_extract_', suffix='.json') as jf:
            self.assertEqual(os.path.basename(jf.name), self.obj.get_files())
            mocked_glob.assert_called_with('url_extract_*.json')


if __name__ == '__main__':
    unittest.main()
