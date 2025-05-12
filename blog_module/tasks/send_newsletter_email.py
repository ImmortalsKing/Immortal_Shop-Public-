from KalaMax_Project.celery_config import app
from utils.email_service import send_email


@app.task(queue='tasks', autoretry_for=(Exception,), default_retry_delay=3, max_retries=3)
def send_newsletter_email(title, email, context):
    try:
        send_email(f'New Blog({title})', to=email, context=context, template_name='emails/newsletter.html')
    except Exception as e:
        newsletter_dead_letter_handle.apply_async(args=[email,str(e)])


@app.task(queue='dead_letter')
def newsletter_dead_letter_handle(email, error_message):
    print(f'Failed to send email to {email}. Error: {error_message}')