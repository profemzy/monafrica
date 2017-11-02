from lib.flask_mailplus import send_template_message
from monafrica.app import create_celery_app

celery = create_celery_app()


@celery.task()
def deliver_feedback_email(name, email, message):
    ctx = {'name': name, 'email': email, 'message': message}

    send_template_message(subject='[Mon Africa] Feedback',
                          sender=name,
                          recipients=[celery.conf.get('MAIL_USERNAME')],
                          reply_to=email,
                          template='feedback/mail/index', ctx=ctx)
    return None
