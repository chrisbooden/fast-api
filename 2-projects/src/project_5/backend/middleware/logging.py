from fastapi import Request, Response
from typing import Awaitable, Callable
from database import SessionLocal
from models import Logs
from datetime import datetime, timezone
import json

# Add a database log entry for 
async def logger(req: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

    # Add a new log entry and add the id to the req object
    log_id = None
    if req.method in ("POST", "PUT", "PATCH", "DELETE"):
        with SessionLocal() as db:
            log = Logs(
                url=req.url.path,
                request_type=req.method,
                query_params=json.dumps(dict(req.query_params)),
                start_time=datetime.now(timezone.utc),
                completed=False
            )

            db.add(log)
            db.commit()
            db.refresh(log)
            log_id = log.log_id
            req.state.log_id = log_id
    else:
        req.state.log_id = None

    # Complete the log entry after the endpoint has been called
    msg = None
    try:
        resp = await call_next(req)
        return resp
    except Exception as e:
        msg = str(e)
        raise
    finally:
        if log_id is not None and req.state.log_id is not None:
            with SessionLocal() as db:
                log = db.query(Logs).get(log_id)
                if log:
                    log.end_time = datetime.now(timezone.utc)
                    log.run_time = int((datetime.now(timezone.utc) - log.start_time).total_seconds() * 1000)
                    log.completed = True
                    if msg is not None: 
                        log.msg = msg[:1000]
                    db.commit()
        

                
                
                

                

     


