from app.settings import DATABASE as db_settings
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(
    db_settings['name'],
    max_connections=32,
    stale_timeout=30,
    host=db_settings['host'],
    user=db_settings['user'],
    password=db_settings['password']
)