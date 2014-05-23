from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
import threading
import os
import time

spoolgore_local = threading.local()

class EmailBackend(BaseEmailBackend):

    __tmp__ = "%s/tmp" % settings.SPOOLGORE_DIRECTORY

    def send_messages(self, email_messages):
        pid = os.getpid()
        tid = threading.current_thread().ident
        num_sent = 0
        if not email_messages:
            return
        for email_message in email_messages:
            if self._send(email_message.message().as_string(), pid, tid):
                num_sent += 1
        return num_sent

    def fsyncspool(self):
        """
        Call fsync() on the spool directory
        """
        fd = -1
        try:
            fd = os.open(settings.SPOOLGORE_DIRECTORY, os.O_RDONLY)
            os.fsync(fd)
        finally:
            if fd > -1: os.close(fd)

    def _send(self, data, pid, tid):
        if not hasattr(spoolgore_local, 'counter'):
            spoolgore_local.counter = 0
        spoolgore_local.counter += 1
        filename = "%f_%s_%d_%d_%d" % (time.time(), time.strftime("%Y.%m.%d.%H.%M.%S"), pid, tid, spoolgore_local.counter)
        tmp = "%s/%s" % (self.__tmp__, filename)
        if not os.path.exists(self.__tmp__):
            os.makedirs(self.__tmp__)
        spool = "%s/%s" % (settings.SPOOLGORE_DIRECTORY, filename)

        with open(tmp, 'w') as f:
            f.write(data)

        try:
            os.link(tmp, spool)
            self.fsyncspool()
        finally:
            os.unlink(tmp)

        return True
