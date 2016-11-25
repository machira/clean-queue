# Clean Queues

The [Python Queues](https://docs.python.org/2/library/queue.html#module-Queue) module does not address a use case where you want your queue consumer to perform some clean up before exiting. Indeed, the example usage in the docs involves use of a daemonic thread, a use case that is only viable when you don't really care about ending the thread context cleanly.

This problem is well described in this stack overflow question: https://stackoverflow.com/questions/3605188/communicating-end-of-queue

 This module is an extension of the threading-Queue and it addresses this problem by exposing a closing mechanism over that Queue. When producers are ready to communicate the end of a queue, they simply close it. The consumer on the other hand can listen for this condition, and exit cleanly at that time.

  Check out the tests for an example of usage.

