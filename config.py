import time
from functools import lru_cache
from colorama import Fore
from socket import *
import netifaces as ni
#from config.logger_config import LoggerConfig
import logging
import os
import signal
class AppConfig():
    def __init__(self):
        self.port_tcp = 5000
        self.port_udp = 6000
        self.max_users = 100
        self.registryWaiting = 100
        self.peerSendTime = 50
        self.hostname = self._hostname_property

    @property
    @lru_cache(maxsize=1)
    def _hostname_property(self):
        try:
            host_result = gethostbyname(gethostname())
            #logger.info(f'Operating System host name is {host_result}')
            return host_result
        except gaierror:
            fallback_result = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
           # logger.info(f'Operating System host name is {fallback_result}')
            return fallback_result
        
obj = AppConfig()
print(Fore.MAGENTA+"The Host Ip address")
print(Fore.MAGENTA+obj.hostname)