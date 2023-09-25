from django.shortcuts import render, redirect
from .models import Package, Student, Message, Question
from .forms import RegisterForm, QuestionForm
from django.contrib import messages
from coinbase_commerce.client import Client
from fx_class import settings
import logging
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required(login_url='login')
def home(request):
	return render(request, 'index.html', {})

def contact(request):
    if request.method == 'POST':
        message=request.POST['message']
        if '?' in message:
            question=Question.objects.create(question=message)
            messages.success(request, ("Question Received"))
        else:
            info=Message.objects.create(name=request.user.username, message=message)
            messages.success(request, ("Message Received"))
        return redirect('contact')
    return render(request, 'contact.html', {})

def classes(request):
    if request.method == 'POST':
        form=QuestionForm(request.POST or None)
        if form.is_valid():
            question=form.cleaned_data['question']
            form.save()
            messages.success(request, ('Kindly await answer'))
            return render(request, 'classes.html', {'question':question})
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = 'http://localhost:8000/'
    product = {
    'name': ' Forex class 1',
        'description': 'A really nice class, online',
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
    product2 = {
    'name': 'Forex class 2',
        'description': 'A really nice class test, private.',
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
    product3 = {
    'name': 'Forex class 3',
        'description': 'A really nice class test, physical.',
        'metadata': {
            'customer_id': request.user.id if request.user.is_authenticated else None,
            'customer_username': request.user.username if request.user.is_authenticated else None,
            'customer_reg': 'Physical class'
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
    charge2 = client.charge.create(**product2)
    hosted_url2 = charge2.hosted_url
    charge3 = client.charge.create(**product3)
    hosted_url3 = charge3.hosted_url
    form=QuestionForm()

    return render(request, 'classes.html', {
        'form':form,
        'domain_url':domain_url,  
        'charge': charge, 
        'hosted_url':hosted_url, 
        'charge2': charge2, 
        'hosted_url2':hosted_url2,
        'charge3': charge3, 
        'hosted_url3':hosted_url3,
        })

def login_user(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('login successful'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in'))
            return redirect('login')
    return render(request, 'login.html', {})

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email exists')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username exists')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_model=User.objects.get(username=username)
                person=authenticate(username=username, password=password)
                login(request, person)
                return HttpResponseRedirect('/')
        else:
            messages.success(request, ('Password do not match.'))
            return render(request, 'register.html', {})
	return render(request, 'register.html', {})

def success_view(request):
    return render(request, 'success.html', {})

def cancel_view(request):
    return render(request, 'cancel.html', {})


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
            class_registered = event['data']['metadata']['customer_reg'] # new
            # TODO: run some custom code here
            #package=Package.objects.all()
            #first=package[0]
            #student_name = customer_username
            #student= Student.objects.create(name=student_name, registering_for=first)
            #return redirect('home')
        #elif event['type'] == 'charge2:confirmed':
            #logger.info('Payment confirmed.')
            #customer_id = event['data']['metadata']['customer_id'] # new
            #customer_username = event['data']['metadata']['customer_username'] # new
            #class_registered = event['data']['metadata']['customer_reg'] # new
            # TODO: run some custom code here
            #package=Package.objects.all()
            #first=package[0]
            #student_name = customer_username
            #student= Student.objects.create(name=student_name, registering_for=first)
            #return redirect('home')
            ####
            if class_registered=='Online class':
                package=Package.objects.all()
                first=package[0]
                student_name = customer_username
                registered = class_registered
                student= Student.objects.create(name=student_name, registering_for=first)
                student.save()
                messages.success(request, ('Payment and registeration successfull'))
                return redirect('home')
                # you can also use 'customer_id' or 'customer_username'
                # to fetch an actual Django user
            elif class_registered=='Physical class':
                package=Package.objects.all()
                second=package[1]
                student_name = customer_username
                registered = class_registered
                student= Student.objects.create(name=student_name, registering_for=second)
                student.save()
                messages.success(request, ('Payment and registeration successfull'))
                return redirect('home')


    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)

def verify(request):
    if request.method=='POST':
        package=Package.objects.all()
        second=package[1]
        name= request.POST['username']
        user=Student.objects.create(name=name, registering_for=second)
        user.save()
        return redirect(verify)
    return render(request, 'verify.html', {})

def packages(request):
    package=Package.objects.all()
    second=package[1]
    return render(request, 'package.html', {'package':package, 'second': second})











