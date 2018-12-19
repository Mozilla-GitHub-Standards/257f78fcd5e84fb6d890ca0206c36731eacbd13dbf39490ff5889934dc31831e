from nhobot import app, scheduler
import atexit
from nhobot.routes import send_newhire_messages, get_auth_zero, updates_from_slack


@atexit.register
def shutdown():
    """
    Register the function to be called on exit
    """
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    print('starting app')
    print('scheduler = {}'.format(scheduler.running))
    if scheduler.running is False:
        scheduler.start()
        # scheduler.add_job(func=send_newhire_messages, trigger='cron', hour='*', minute='*/10')
        # scheduler.add_job(func=get_auth_zero, trigger='cron', hour=0, minute=0)
        # scheduler.add_job(func=updates_from_slack, trigger='cron', hour=0, minute=5)
    app.debug = False
    app.use_reloader=False
    app.jinja_env.cache = {}
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0')
