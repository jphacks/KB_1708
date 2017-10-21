import time

from celery import task
from celery.signals import task_revoked


class DevideInt:
    def __init__(self):
        print('a')

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('__exit__')
        print('exc_type : ', exc_type, 'exc_value: ', exc_value, 'traceback: ', traceback)
        return True

@task
def test():
    # random task
    counter = 0
    with DevideInt():
        while counter < 50:
            print(str(counter))
            time.sleep(1)
            counter += 1


def on_task_revoked(*args, **kwargs):
    print(str(kwargs))
    print('task_revoked')
    with open('test.txt', 'w') as f:
        f.write('task_revoked')
task_revoked.connect(on_task_revoked, dispatch_uid='on_task_revoked')