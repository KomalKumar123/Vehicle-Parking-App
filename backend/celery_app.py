from celery import Celery

# Create the core Celery instance.
# The first argument is the name of the current module.
# This instance is not yet configured with the Flask app context.
celery = Celery(__name__)