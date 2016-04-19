from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.core.management import call_command


class StartupMiddleware(object):

    def __init__(self):
        up = False
        print 'check..................................'
        while not up:
            try:
                # # The following db settings name is django 1.2.  django < 1.2 will use settings.DATABASE_NAME
                # if settings.DATABASES['default']['NAME'] == ':memory:':
                call_command('syncdb', interactive=False)
                call_command('collectstatic', interactive=False)
                up = True
            except:
                print 'waiting...'
                time.sleep(1)

        raise MiddlewareNotUsed('Startup complete')
