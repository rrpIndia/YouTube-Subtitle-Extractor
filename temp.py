import tempfile as tf

def h():
   with tf.NamedTemporaryFile(prefix='url_extract_1', suffix='.json') as jf:
      file = os.path.basename(jf.file)
      print(file)

h()
