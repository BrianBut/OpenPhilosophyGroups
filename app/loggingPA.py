import logging
import sys

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

duty_handler = logging.FileHandler('logs.lplog')
duty_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
duty_handler.setFormatter(formatter)

logger.addHandler(duty_handler)

err_handler = logging.StreamHandler(sys.stderr)
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(formatter)

logger.addHandler(err_handler)
