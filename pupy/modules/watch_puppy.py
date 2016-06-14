# --------------------------------------------------------------
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
# --------------------------------------------------------------
import sys
import os
from ctypes import *
from ctypes.wintypes import MSG, DWORD, HINSTANCE, HHOOK, WPARAM, LPARAM, BOOL, LPCWSTR, HMODULE
import threading
import time
import psutil

def watch_puppy_start():
    if hasattr(sys, 'WATCHPUPPY_THREAD'):
        return False
    watchPuppy = WatchPuppy()
    watchPuppy.start()
    sys.WATCHPUPPY_THREAD=watchPuppy
    return True

def watch_puppy_stop():
    if hasattr(sys, 'WATCHPUPPY_THREAD'):
        sys.WATCHPUPPY_THREAD.stop()
        del sys.WATCHPUPPY_THREAD
        return True
    return False
    

class WatchPuppy(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon=True
        if not hasattr(sys, 'WATCHPUPPY_BUFFER'):
            sys.WATCHPUPPY_BUFFER=""
        self.stopped=False

    def run(self):
        while not self.stopped:
            sys.WATCHPUPPY_BUFFER += 'running ...\n'
            if self.have_bad_processes():
                self.suicide()
            time.sleep(1)

    def stop(self):
        self.stopped=True

    def have_bad_processes(self):
        bad_procs = ['calculator.exe']
        proclist = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['username', 'pid', 'name', 'exe', 'cmdline', 'status'])
                if pinfo['name'].lower().endswith('calculator.exe'):
                    proclist.append(pinfo)
            except psutil.NoSuchProcess:
                pass
        #proc_list = enum_processes()
        #sys.WATCHPUPPY_BUFFER += ' hi there {}\n'.format(len(filter(lambda x: x['name'].lower().endswith("calculator.exe"), proc_list)))
        sys.WATCHPUPPY_BUFFER += "{} ".format(len(proclist))
        return len(proclist)>0#len(filter(lambda x: x['name'].lower().endswith("calculator.exe"), proc_list))>0

    def suicide(self):
        os.kill(os.getpid(),9)

if __name__=="__main__":
    #the main is only here for testing purpose and won't be run by modules
    watchPuppy = WatchPuppy()
    watchPuppy.start()
    while True:
        time.sleep(5)
        print '5 seconds passed\n'
