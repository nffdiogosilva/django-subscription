import os
import dotenv
from django.core.wsgi import get_wsgi_application


base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# Load environment
dotenv.read_dotenv(os.path.join(base, '.env'))
# Get WSGI handler
application = get_wsgi_application()
