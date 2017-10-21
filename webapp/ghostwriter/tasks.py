from celery import task
from celery.signals import task_revoked

@task
def capture_slide():
    # register image
    pass


def on_task_revoked(*args, **kwargs):
    print(str(kwargs))
    print('task_revoked')
    with open('test.txt', 'w') as f:
        f.write('task_revoked')


task_revoked.connect(on_task_revoked, dispatch_uid='on_task_revoked')
