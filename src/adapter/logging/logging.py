import logging
from datetime import datetime
import colorlog

class LoggerHandler:
    def __init__(self, context = "Log", level= logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        handler = logging.StreamHandler()
        color_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )
        handler.setFormatter(color_formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)
        
        self.context = context

    def _log(self, level, message):
        timeestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        full_message = f"{timeestamp} - {self.context} ->> {message}"

        if level == "INFO":
            self.logger.info(full_message)
        elif level == "DEBUG":
            self.logger.debug(full_message)
        elif level == "WARNING":
            self.logger.warning(full_message)
        elif level == "ERROR":
            self.logger.error(full_message)
        elif level == "CRITICAL":
            self.logger.critical(full_message)

    def INFO(self, message):
        self._log("INFO", message)
    
    def DEBUG(self, message):
        self._log("DEBUG", message)
    
    def WARNING(self, message):
        self._log("WARNING", message)
    
    def ERROR(self, message):
        self._log("ERROR", message)
    
    def CRITICAL(self, message):
        self._log("CRITICAL", message)
    
    