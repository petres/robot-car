import time
import threading
import logging
import requests

logger = logging.getLogger('camera')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('instance/camera.log', mode='w')  
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

with open('assets/dummy-800x600.jpg', 'rb') as f:
    dummy_jpeg = f.read()

class Camera(object):
    url = None
    stream = None
    recv_t = None
    stop = False
    boundary = None
    frame = None
    frame_time = None
    
    def __init__(self, url):
        self.url = url
        self.frame = dummy_jpeg
        
    def connect(self):
        if self.isStreaming():
            logger.warning(f'not connecting, already streaming')
            return
        
        self.stop = False
        logger.debug(f'connecting to stream `{self.url}`')
        self.stream = requests.get(self.url, stream=True)
        
        if self.stream.status_code == 200:
            content_type = self.stream.headers['content-type']
            self.boundary = b"--" + content_type.split("boundary=")[-1].encode()
    
            self.recv_t = threading.Thread(target=self._recv, args=[])    
            self.recv_t.start()
        else:
            m = f'status_code != 200'
            logger.warning(m)
            raise Exception(m)
        
    def disconnect(self):
        self.stop = True
        logger.debug(f'waiting for communication threads')
        self.recv_t.join()
        logger.debug(f'closing stream')
        self.stream.close()
        self.frame = dummy_jpeg
        
    def isStreaming(self):
        # return not (self.stream is None or self.stream.raw is None or self.stream.raw.closed)
        return self.frame_time is not None and time.time_ns() - self.frame_time < 2_000_000_000
    
    def get_frame(self):
        return self.frame
        
    def _recv(self):
        buffer = bytes()
        for chunk in self.stream.iter_content(1024):
            if self.stop:
                break
            buffer += chunk
            while self.boundary in buffer:
                part_data, buffer = buffer.split(self.boundary, 1)
                if b'Content-Type: image/jpeg' in part_data:
                    jpeg_part = part_data.split(b'\r\n\r\n')[1].rstrip(b'\r\n')
                    self.frame = jpeg_part
                    self.frame_time = time.time_ns()



    
