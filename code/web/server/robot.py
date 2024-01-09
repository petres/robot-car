import socket
import time
import queue
import threading
import logging

logging.basicConfig(filename='robot.log', filemode='w', level=logging.DEBUG)

class Robot(object):    
    heartbeat_message = "{Heartbeat}"
    heartbeat_freq = 1000
    
    com_s = None
    com_t = None
        
    last_heartbeat_time = 0
    
    send_q = queue.Queue()
    got_q = queue.Queue()

    stop = False
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def connect(self):
        self.stop = False
        self.com_s = socket.socket()
        logging.debug(f'socket connecting to {(self.host, self.port)}')
        self.com_s.connect((self.host, self.port))  # connect to the server
        self.com_t = threading.Thread(target=self._keepAliveAndSendMessages, args=[])
        self.com_t.start()
        
    def disconnect(self):
        self.stop = True
        logging.debug(f'waiting for message thread')
        self.com_t.join()
        logging.debug(f'closing socket')
        self.com_s.close()
        
    def isAlive(self):
        # print(self.last_heartbeat_time)
        return time.time_ns() - self.last_heartbeat_time < 2_000_000_000
        
    def send(self, m, r = False):
        self.send_q.put(m)
        if r:
            return self.got_q.get()
        
    def _keepAliveAndSendMessages(self):
        while not self.stop:
            self._checkHeartbeat()
            
            message = self.com_s.recv(1024).decode()
            if message == self.heartbeat_message:
                logging.debug('received heartbeat')
            else:
                logging.info(f'received message: `{message}`')
                self.got_q.put(message)
                
            try:
                message = self.send_q.get_nowait()
                logging.info(f'send message: `{message}`')
                self.com_s.send(message.encode())
            except queue.Empty:
                time.sleep(0.01)  # sleep if no items in queue
    
    def _checkHeartbeat(self):
        if time.time_ns() - self.last_heartbeat_time > 1_000_000 * self.heartbeat_freq:
            self._sendHeartbeat()
            
    def _sendHeartbeat(self):
        logging.debug('send heartbeat')
        self.com_s.send(self.heartbeat_message.encode())
        self.last_heartbeat_time = time.time_ns()

