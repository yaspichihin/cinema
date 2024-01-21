import queue


def transform(queue_transform: queue.Queue, queue_load: queue.Queue) -> None:
    for _ in range(queue_transform.qsize()):
        queue_load.put(queue_transform.get())
