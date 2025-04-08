import logging
import socket
import sys
from datetime import datetime

# Custom handler that silently fails if logging to Loki fails
class SafeHandler(logging.Handler):
    def __init__(self, target_handler):
        super().__init__()
        self.target_handler = target_handler
        
    def emit(self, record):
        try:
            self.target_handler.emit(record)
        except Exception:
            # Silently fail - explicitly suppress the handleError call
            pass

    def handleError(self, record):
        # Override handleError to prevent any error output
        pass

def setup_logging():
    
    logger = logging.getLogger("api")
    
    # Try setting up Loki (optional)
    try:
        import logging_loki
        # Using host.docker.internal instead of localhost to properly reach Loki container from host machine
        loki_url = "http://localhost:3100/loki/api/v1/push"
        
        logger.info(f"Attempting to connect to Loki at {loki_url}")
        
        loki_direct_handler = logging_loki.LokiHandler(
            url=loki_url, 
            tags={"service": "api-server", "host": socket.gethostname()},
            version="1",
        )
        # Wrap the Loki handler in our SafeHandler to prevent exceptions
        loki_handler = SafeHandler(loki_direct_handler)
        logger.addHandler(loki_handler)
        logger.info("Successfully connected to Loki logging service")
    except Exception as e:
        # Log the exception but continue without Loki
        logger.warning(f"Failed to connect to Loki: {str(e)}")
    
    # Log startup info
    logger.info(f"Initializing application on {socket.gethostname()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current time: {datetime.now().isoformat()}")
    
    return logger