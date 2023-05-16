from celery import Celery
import time

celery = Celery("app", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task(bind=True)
def long_task(self):
    total = 100
    for i in range(total):
        time.sleep(1)  # replace with real work
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total})
    return {'current': 100, 'total': 100, 'status': 'Task completed!'}
