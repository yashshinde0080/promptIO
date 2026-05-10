from celery import Celery
from config import settings

celery_app = Celery(
    "promptio",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "workers.evaluation_worker",
        "workers.ai_worker",
        "workers.reporting_worker",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_routes={
        "workers.evaluation_worker.*": {"queue": "evaluation"},
        "workers.ai_worker.*": {"queue": "ai"},
        "workers.reporting_worker.*": {"queue": "reporting"},
    },
    beat_schedule={
        "cleanup-old-runs": {
            "task": "workers.ai_worker.cleanup_old_runs",
            "schedule": 86400,
        },
    },
)