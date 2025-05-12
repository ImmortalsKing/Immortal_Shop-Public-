from KalaMax_Project.celery_config import app
from account_module.models import User
from site_module.models import SiteSettings
from utils.email_service import send_email


@app.task(queue='tasks', autoretry_for=(Exception,), default_retry_delay=3, max_retries=3)
def send_activation_email(user_id):
    try:
        new_user = User.objects.get(id=user_id)
        site_setting = SiteSettings.objects.filter(is_main_setting=True).first()
        site_url = site_setting.site_url if site_setting else 'http://localhost:8000'
        send_email('Account Activation', new_user.email, {'user': new_user,'site_url':site_url}, 'emails/activate_account.html')
    except User.DoesNotExist:
        print(f'User with id {user_id} does not exist')
    except Exception as e:
        dead_letter_handle.apply_async(args=[user_id, str(e)])


@app.task(queue='tasks', autoretry_for=(Exception,), default_retry_delay=3, max_retries=3)
def send_reset_password_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        site_setting = SiteSettings.objects.filter(is_main_setting=True).first()
        site_url = site_setting.site_url if site_setting else 'http://localhost:8000'
        send_email('Password Recovery', user.email, {'user': user,'site_url':site_url}, 'emails/forgot_password.html')
    except User.DoesNotExist:
        print(f'User with id {user_id} does not exist')
    except Exception as e:
        dead_letter_handle.apply_async(args=[user_id, str(e)])


@app.task(queue='dead_letter')
def dead_letter_handle(user_id, error_message):
    print(f'Failed to send email for user with id: {user_id}. Error: {error_message}')