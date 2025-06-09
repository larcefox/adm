from flask.cli import FlaskGroup
from threading import Thread
from loguru import logger
from src import app
from lib.websocket_server import run_websocket
from lib.reload_canvas import Worker


logger.add('./logs/manage.log', format="{time} {level} {message}", level="INFO", retention="10 days")
cli = FlaskGroup(app)

if __name__ == "__main__":
    
    ws_thread = Thread(target = run_websocket)
    canvas_thread = Worker()
    try:
        canvas_thread.start()
        ws_thread.start()
        # ws_thread.join()
        logger.info("Websocket trying to start:", ws_thread)
        logger.info("Canvas reload trying to start:", canvas_thread)
        
    except OSError as e:
        logger.info("Websocket already started")
    
    cli()