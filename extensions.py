from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Para evitar ataques de fuerza bruta
# Hace que limite las peticiones por dia y por hora por IP address
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "100 per hour"],
    storage_uri="memory://" 
)
