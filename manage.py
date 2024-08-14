from flask.cli import FlaskGroup
import subprocess
from loguru import logger
from src import app


logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")
cli = FlaskGroup(app)

if __name__ == "__main__":
    command = ["/home/larce/projects/idm/.venv/bin/python", "/home/larce/projects/idm/lib/websocket_server.py"]
    try:
        process = subprocess.Popen(command)
        logger.info("Websocket trying to start:", process)
        
    except OSError as e:
        logger.info("Websocket already started")
    
    cli()