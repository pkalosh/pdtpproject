from django import template
import datetime
from app.models import *
import datetime
today = datetime.datetime.today()

register =template.Library()
@register.inclusion_tag('yearslinks.html')

def years_list(event=None):
	top =PdtpYear.objects.order_by('-year')[0]
	return {'years':PdtpYear.objects.all().exclude(id=top.id),'top_year':PdtpYear.objects.order_by('-year')[0]}
