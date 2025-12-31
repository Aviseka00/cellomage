from datetime import datetime
from database.mongo import mongo

def log_event(
    action,
    image_name,
    model_used,
    cell_count,
    confluency,
    view_mode,
    ip_address,
    status="SUCCESS"
):
    mongo.db.audit_logs.insert_one({
        "timestamp": datetime.utcnow(),
        "action": action,
        "image_name": image_name,
        "model_used": model_used,
        "cell_count": cell_count,
        "confluency": confluency,
        "view_mode": view_mode,
        "ip_address": ip_address,
        "status": status
    })
