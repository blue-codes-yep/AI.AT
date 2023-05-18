from celery import Celery
import time

celery = Celery("app", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.update(task_track_started=True)

from utils.video_utils import create_video
