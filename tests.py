# class


# I should be able to initialize a queue + consumers, add stuff to it, and when I close that queue, the consumers
# will do some cleanup and exit cleanly.
# A closed queue cannot be reopened.
# Every task should be executed once, or retried.
# Should work with: - multiple consumers and producers.
# After resuming execution on a closed queue, there should be exactly one thread left- the main thread.
from threading import Thread
from unittest import TestCase
from Queue import Empty
from time import sleep
from CloseableQueue import CloseableQueue, ClosedQueueException
import threading


class CloseableQueueTest(TestCase):
    def setUp(self):
        self.queue = CloseableQueue()

    def _do_work(self, i):
        return i + 1

    def _worker(self):
        while True:
            item = self.queue.get()
            self._do_work(item)
            self.queue.task_done()

    def _addToQueue(self, item):
        self.queue.put(item)

    def test_new_queue_should_be_empty(self):
        self.assertTrue(self.queue.empty())

    def test_queue_with_one_item_should_not_be_empty(self):
        self.queue.put(1)
        self.assertFalse(self.queue.empty())

    def test_shouldProcessAllMessagesOnQueue(self):
        t = Thread(target=self._worker)
        t.daemon = True
        for item in range(100):
            self._addToQueue(item)
        t.start()
        self.queue.join()
        self.assertTrue(self.queue.empty())

    def test_new_queue_should_be_open(self):
        self.assertFalse(self.queue.closed())

    def test_queue_should_be_closeable(self):
        self.queue.close()
        self.assertTrue(self.queue.closed())

    def test_can_close_multiple_times(self):
        t1 = Thread(target=self.queue.close)
        t1.start()
        t2 = Thread(target=self.queue.close)
        t2.start()
        t1.join()
        t2.join()

    def test_should_not_add_to_closed_queue(self):
        self.queue.close()
        with self.assertRaises(ClosedQueueException):
            self.queue.put(10)

    def test_thread_can_clean_up(self):

        def work():
            while not self.queue.closed():
                try:
                    _ = self.queue.get(timeout=3)
                except Empty:
                    pass

        t = Thread(target=work)
        t.setDaemon(True)
        t.start()
        self.assertEqual(threading.active_count(), 2)
        self.queue.close()
        sleep(6)
        self.assertEqual(threading.active_count(), 1)
