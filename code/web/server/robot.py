import socket
import time
import queue
import threading
import logging

logger = logging.getLogger('robot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('robot.log', mode='w')  
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# logging.basicConfig(filename='robot.log', filemode='w', level=logging.DEBUG)

class Robot(object):    
    heartbeat_message = "{Heartbeat}"
    heartbeat_freq = 3000
    
    socket = None
    
    send_t = None
    recv_t = None
        
    _last_heartbeat_time = 0
    
    send_q = queue.Queue()
    recv_q = queue.Queue()

    stop = False
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def connect(self):
        self.stop = False
        self.socket = socket.socket()
        # self.socket.settimeout(0.02)
        logger.debug(f'socket connecting to {(self.host, self.port)}')
        try:
            self.socket.connect((self.host, self.port))  # connect to the server
        except Exception as e:
            logger.warning(f'error occured while connecting: {e}')
            raise e
        self.recv_t = threading.Thread(target=self._recv, args=[])
        self.send_t = threading.Thread(target=self._send, args=[])
        self.recv_t.start()
        self.send_t.start()
        
    def disconnect(self):
        self.stop = True
        logger.debug(f'waiting for communication threads')
        self.recv_t.join()
        self.send_t.join()
        logger.debug(f'closing socket')
        self.socket.close()
        
    def isAlive(self):
        # print(self._last_heartbeat_time)
        return time.time_ns() - self._last_heartbeat_time < 4_000_000_000
        
    def send(self, m, r = False):
        self.send_q.put(m)
        # if r:
        #     return self.recv_q.get()
        
    def _send(self):
        while not self.stop:
            self._checkHeartbeat()
                
            try:
                message = self.send_q.get_nowait()
                logger.info(f'send message: `{message}`')
                self.socket.send(message.encode())
            except queue.Empty:
                # pass
                time.sleep(0.05)  # sleep if no items in queue
    
    def _checkHeartbeat(self):
        if time.time_ns() - self._last_heartbeat_time > 1_000_000 * self.heartbeat_freq:
            self._sendHeartbeat()
            
    def _sendHeartbeat(self):
        logger.debug('send heartbeat')
        self.socket.send(self.heartbeat_message.encode())
        self._last_heartbeat_time = time.time_ns()

    def _recv(self):
        while not self.stop:
            message = self.socket.recv(1024).decode()
            if message == self.heartbeat_message:
                logger.debug('received heartbeat')
            else:
                logger.info(f'received message: `{message}`')
                self.recv_q.put(message)

                
    # def _keepAliveAndSendMessages(self):
    #     while not self.stop:
    #         self._checkHeartbeat()
            
    #         try:
    #             message = self.socket.recv(1024).decode()
    #             if message == self.heartbeat_message:
    #                 logging.debug('received heartbeat')
    #             else:
    #                 logging.info(f'received message: `{message}`')
    #                 self.recv_q.put(message)
    #         except socket.timeout:
    #             pass
                
    #         try:
    #             message = self.send_q.get_nowait()
    #             logging.info(f'send message: `{message}`')
    #             self.socket.send(message.encode())
    #         except queue.Empty:
    #             # pass
    #             time.sleep(0.05)  # sleep if no items in queue
