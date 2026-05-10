from workers.celery_app import celery_app
import asyncio
import structlog

logger = structlog.get_logger(__name__)


@celery_app.task(name="workers.evaluation_worker.run_async_evaluation", bind=True, max_retries=3)
def run_async_evaluation(self, prompt_content: str, prompt_id: str = None, model: str = None):
    """Async evaluation worker task"""
    try:
        async def _run():
            from services.evaluation_service import EvaluationService
            service = EvaluationService()
            return await service.run_evaluation(
                prompt_content=prompt_content,
                prompt_id=prompt_id,
                model=model,
                run_full=True,
            )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_run())
        loop.close()

        logger.info("Async evaluation completed", prompt_id=prompt_id)
        return result

    except Exception as e:
        logger.error("Evaluation worker failed", error=str(e), prompt_id=prompt_id)
        raise self.retry(exc=e, countdown=60)