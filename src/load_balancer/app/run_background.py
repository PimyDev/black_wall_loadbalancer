import asyncio
from datetime import datetime

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from app.services.flood import start_flood
from app.services.logger import configure_logger
from app.services.target_service import check_inactive_target_services


def main():
    configure_logger(capture_exceptions=True)

    scheduler = AsyncIOScheduler(timezone=pytz.UTC)
    scheduler.add_job(check_inactive_target_services, 'interval', seconds=10, next_run_time=datetime.utcnow())
    scheduler.add_job(start_flood)
    scheduler.start()

    logger.info("Background tasks started success")

    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == "__main__":
    main()
