import socket
import time
import queue
import threading
import logging

logger = logging.getLogger('robot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('instance/robot.log', mode='w')  
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# logging.basicConfig(filename='robot.log', filemode='w', level=logging.DEBUG)

class Robot(object):    
    heartbeat_message = "{Heartbeat}"
    heartbeat_freq = 1000
    
    socket = None
    
    send_t = None
    recv_t = None
        
    _last_heartbeat_send_time = None
    _last_heartbeat_recv_time = None
    
    send_q = queue.Queue()
    recv_q = queue.Queue()

    stop = False
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def connect(self):
        if self.isAlive():
            logger.warning(f'not connecting, already alive')
            return
            
        self.stop = False
        self.socket = socket.socket()
        # self.socket.settimeout(0.02)
        logger.debug(f'socket connecting to {(self.host, self.port)}')
        try:
            self.socket.connect((self.host, self.port))  # connect to the server
        except Exception as e:
            logger.warning(f'error occured while connecting: {e}')
            raise e
        
        self._last_heartbeat_send_time = None
        self._last_heartbeat_recv_time = None
        
        self.recv_t = threading.Thread(target=self._recv, args=[])
        self.send_t = threading.Thread(target=self._send, args=[])
        
        self.recv_t.start()
        self.send_t.start()
        
    def disconnect(self):
        self.stop = True
        
        if self.recv_t is not None and self.recv_t.is_alive():
            logger.debug(f'joining for recv communication thread')
            self.recv_t.join()
            
        if self.send_t is not None and self.send_t.is_alive():
            logger.debug(f'joining for send communication thread')
            self.send_t.join()
            
        if self.socket is not None:
            logger.debug(f'closing socket')
            self.socket.close()
            self.socket = None
        
    def isAlive(self):
        # print(self._last_heartbeat_send_time)
        return self._last_heartbeat_recv_time is not None and time.time_ns() - self._last_heartbeat_recv_time < 2_000_000_000
        
    def send(self, m):
        self.send_q.put(m)
        
    def _send(self):
        self._sendHeartbeat()
        while not self.stop:
            self._checkHeartbeat()
            try:
                message = self.send_q.get_nowait()
                logger.info(f'send message: `{message}`')
                self.socket.send(message.encode())
            except queue.Empty:
                time.sleep(0.02) 
    
    def _checkHeartbeat(self):
        if time.time_ns() - self._last_heartbeat_send_time > 1_000_000 * self.heartbeat_freq:
            self._sendHeartbeat()
            
    def _sendHeartbeat(self):
        logger.debug('send heartbeat')
        self.socket.send(self.heartbeat_message.encode())
        self._last_heartbeat_send_time = time.time_ns()

    def _recv(self):
        while not self.stop:
            message = self.socket.recv(1024).decode()
            if message == self.heartbeat_message:
                logger.debug('received heartbeat')
                self._last_heartbeat_recv_time = time.time_ns()
            else:
                logger.info(f'received message: `{message}`')
                self.recv_q.put(message)
            
            time.sleep(0.10)
