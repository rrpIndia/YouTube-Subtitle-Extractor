import unittest
import re

#from main import get_id
def get_id(url:str)->str:
   data = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
   if data:
       return data[0]
   return None 

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
if __name__ == '__main__':
    unittest.main()

