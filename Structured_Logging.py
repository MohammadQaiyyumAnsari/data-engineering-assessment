import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage()
        }
        if hasattr(record, 'extra_data'):
            log_entry['context'] = record.extra_data
        return json.dumps(log_entry)

logger = logging.getLogger("ETLPipeline")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# Sample run
logger.info("Pipeline started", extra={'extra_data': {'stage': 'INIT', 'source': 'orders.csv'}})
logger.info("Transformation finished", extra={'extra_data': {'rows_in': 15, 'rows_out': 15}})
logger.info("Pipeline completed successfully", extra={'extra_data': {'status': 'SUCCESS'}})