from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

DEFAULT = "default"

jobstores = {
    DEFAULT: MemoryJobStore()
}
executors = {DEFAULT: AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 20}

scheduler = AsyncIOScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults
)


async def on_startup(_dispatcher: Dispatcher):
    scheduler.start()


async def on_shutdown(_dispatcher: Dispatcher):
    scheduler.shutdown()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
