from Queue import Queue
from threading import Lock


class ClosedQueueException(RuntimeError):
    pass


class CloseableQueue(Queue, object):
    def __init__(self):
        self._close_lock = Lock()
        self._closed = False
        Queue.__init__(self)

    def put(self, item, **kwargs):
        if self._closed:
            raise ClosedQueueException("Attempting to put into an already closed queue")
        super(CloseableQueue, self).put(item, **kwargs)

    def close(self):
        self._close_lock.acquire()
        self._closed = True
        self._close_lock.release()

    def closed(self):
        return self._closed
