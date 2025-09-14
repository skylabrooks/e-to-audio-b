import logging
import subprocess

import redis
from apscheduler.schedulers.background import BackgroundScheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Redis client
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def refresh_voice_data():
    """
    Refreshes voice data by running the seeding script and clearing the cache.
    """
    try:
        logger.info("Starting voice data refresh job.")

        # Run the seeding script
        subprocess.run(["python", "Backend/scripts/seed_voices.py"], check=True)
        logger.info("Successfully executed seed_voices.py script.")

        # Clear the Redis cache
        redis_client.flushdb()
        logger.info("Redis cache cleared successfully.")

        logger.info("Voice data refresh job completed.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing seed_voices.py: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during the refresh job: {e}")


def initialize_scheduler():
    """
    Initializes and starts the background scheduler.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_voice_data, "interval", days=1)
    scheduler.start()
    logger.info("Scheduler initialized and started.")
    return scheduler
