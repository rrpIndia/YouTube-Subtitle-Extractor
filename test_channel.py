import unittest
from channel import ChannelFile
<<<<<<< HEAD
from unittest.mock import Mock, patch

class TestIsValidYtChannel(unittest.TestCase):
    def test_valid_full(self):
        self.obj = ChannelFile('test_file.txt')
        channel = 'https://www.youtube.com/channel/fireship'
        with patch('requests.get') as mocked_request:
            mocked_request.return_value.status_code = 200
            self.assertTrue(self.obj.is_valid_yt_channel(channel))
            mocked_request.assert_called_once_with(channel)

    def test_non_valid(self):
        self.obj = ChannelFile('test_file.txt')
        self.assertFalse(self.obj.is_valid_yt_channel('Hi'))

    def test_valid(self):
        self.obj = ChannelFile('test_file.txt')
        channel = 'https://www.youtube.com/c/fireship'
        with patch('requests.get') as mocked_request:
=======
from unittest.mock import Mock

class TestIsValidYtChannel(unittest.TestCase):
    def setUp(self):
        self.obj = ChannelFile('test_file.txt')
        self.mocked_request = Mock('channel.requests')
        self.mocked_request.get.status_code = 200

    def test_empty(self):
        self.assertFalse(self.obj.is_valid_yt_channel(''))

    def test_non_valid(self):
        self.assertFalse(self.obj.is_valid_yt_channel('Hi'))

    def test_valid(self):
        channel = 'https://www.youtube.com/c/fireship'
        self.assertTrue(self.obj.is_valid_yt_channel(channel))

    def test_mobile_valid(self):
        channel = 'https://m.youtube.com/c/fireship'
        self.assertTrue(self.obj.is_valid_yt_channel(channel))




if __name__ == '__main__':
    unittest.main()
ed_request:
>>>>>>> 7a4526e (nothimg)
            mocked_request.return_value.status_code = 200
            self.assertTrue(self.obj.is_valid_yt_channel(channel))
            mocked_request.assert_called_once_with(channel)

    def test_mobile_valid(self):
        self.obj = ChannelFile('test_file.txt')
        channel = 'https://m.youtube.com/c/fireship'
        with patch('requests.get') as mocked_request:
            mocked_request.return_value.status_code = 200
            self.assertTrue(self.obj.is_valid_yt_channel(channel))
            mocked_request.assert_called_once_with(channel)



if __name__ == '__main__':
    unittest.main()
