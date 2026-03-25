from slowapi import Limiter
from slowapi.util import get_remote_address

# get_remote_address extracts the client's IP address
# from the request — used as the identifier for rate limiting
# so limits apply per IP, not globally
limiter = Limiter(key_func=get_remote_address)
