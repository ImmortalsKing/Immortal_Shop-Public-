from KalaMax_Project.celery_config import app
from account_module.models import User
from site_module.models import SiteSettings
from utils.email_service import send_email


@app.task(queue='tasks', autoretry_for=(Exception,), default_retry_delay=3, max_retries=3)
def update_email(user_id, new_email):
    try:
        current_user = User.objects.get(id=user_id)
        site_setting = SiteSettings.objects.filter(is_main_setting=True).first()
        site_url = site_setting.site_url if site_setting else 'http://localhost:8000'
        send_email('Update Email', new_email, {'user': current_user, 'site_url':site_url}, 'emails/update_email.html')
    except User.DoesNotExist:
        print(f'User with id {user_id} does not exist')
    except Exception as e:
        update_email_dead_letter_handle.apply_async(args=[user_id, str(e)])


@app.task(queue='dead_letter')
def update_email_dead_letter_handle(user_id, error_message):
    print(f'Failed to send email for user with id: {user_id}. Error: {error_message}')