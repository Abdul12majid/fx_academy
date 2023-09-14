from django.shortcuts import render, redirect
from .models import Package, Student
from .forms import RegisterForm
from django.contrib import messages
from coinbase_commerce.client import Client
from fx_class import settings
import logging
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods



# Create your views here.
def home(request):
	return render(request, 'index.html', {})

def contact(request):
	return render(request, 'contact.html', {})

def classes(request):
	client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
	domain_url = 'http://localhost:8000/'
	product = {
		'name': 'Forex class',
		'description': 'A really nice class.',
		'metadata': {
			'customer_id': request.user.id if request.user.is_authenticated else None,
			'customer_username': request.user.username if request.user.is_authenticated else None,
		},
		'local_price': {
			'amount': '0.50',
			'currency': 'USD'
		},
		'pricing_type': 'fixed_price',
		'redirect_url': domain_url + 'success/',
		'cancel_url': domain_url + 'cancel/',
		}
	charge = client.charge.create(**product)
	hosted_url = charge.hosted_url
	form=RegisterForm()
	#if request.method=='POST':
	#	form=RegisterForm(request.POST)
	#	if form.is_valid():
	#		form.save()
	#		messages.success(request, ("You have successfully registered"))
	#		return redirect('classes')
	#else:
	#	form=RegisterForm()
	return render(request, 'classes.html', {'form':form, 'charge': charge, 'domain_url':domain_url, 'hosted_url':hosted_url})

def login_user(request):
	return render(request, 'login.html', {})

def register(request):
	return render(request, 'register.html', {})

def success_view(request):
    return render(request, 'success.html', {})

def cancel_view(request):
    return render(request, 'cancel.html', {})

def payment(request):
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = 'http://localhost:8000/'
    product = {
        'name': 'Forex class',
        'description': 'A really nice class.',
        'metadata': {
        'customer_id': request.user.id if request.user.is_authenticated else None,
        'customer_username': request.user.username if request.user.is_authenticated else None,
    },
        'local_price': {
            'amount': '0.50',
            'currency': 'USD'
        },
        'pricing_type': 'fixed_price',
        'redirect_url': domain_url + 'success/',
        'cancel_url': domain_url + 'cancel/',
    }
    charge = client.charge.create(**product)

    return render(request, 'classes.html', {
        'charge': charge,
    })


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks

        if event['type'] == 'charge:confirmed':
            logger.info('Payment confirmed.')
            customer_id = event['data']['metadata']['customer_id'] # new
            customer_username = event['data']['metadata']['customer_username'] # new
            # TODO: run some custom code here
            messages.success(request, ('Payment successfull'))
            # you can also use 'customer_id' or 'customer_username'
            # to fetch an actual Django user

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)




    