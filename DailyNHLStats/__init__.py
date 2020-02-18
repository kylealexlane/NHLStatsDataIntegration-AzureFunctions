import datetime
import logging
import azure.functions as func

from .production.daily.dailyImport import run_import_today
from .production.transformData.adjustShots import AdjustShots



def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    run_import_today()
    # AdjustShots('2020-02-15', '2020-02-19')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
