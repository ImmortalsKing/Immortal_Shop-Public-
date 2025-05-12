from django.contrib import messages
from django.views.generic import CreateView

from contact_module.forms import ContactUsModelForm
from site_module.models import SiteSettings


# Create your views here.

class ContactUsView(CreateView):
    template_name = 'contact_module/contact_us.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data()
        context ['settings'] = SiteSettings.objects.filter(is_main_setting=True).first()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,'Your comment has been sent successfully!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request,'An Error Occurred while sending your comment! check fields below please. ')
        return response