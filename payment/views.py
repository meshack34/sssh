from django.shortcuts import render, redirect
from sub_part.models import  *
import razorpay
# Create your views here.
from django.contrib import messages
from .mpesa_payments import *

def fees_payment(request,pk):
    general_setting = GeneralSetting.objects.all().last()
    payment_key=PaymentKeys.objects.all().last()
    fees_records=FeesAssign.objects.get(id=pk)
    if general_setting.country == 'India':
        name = request.user.first_name
        amount = int(fees_records.fees.amount) * 100
        # create Razorpay client
        client = razorpay.Client(auth=(payment_key.razorpay_key_id, payment_key.razorpay_key_secret))

        # create order
        response_payment = client.order.create(dict(amount=amount, currency='INR') )

        order_id = response_payment['id']
        order_status = response_payment['status']
        return render(request, 'payment/fees_payment.html',{'fees_records':fees_records, 'payment': response_payment,'payment_key':payment_key})
    elif general_setting.country == 'Kenya':
        if request.method=='POST':
            number=request.POST.get('phone_number')
            result = mpesa_stk_push(int(fees_records.fees.amount),number,request.user.first_name)
            print(result)
            messages.warning(request, result['errorMessage'])
        sudent_records= StudentAdmission.objects.filter(user_parent=request.user)
        return render(request, 'payment/fees_payment.html',{'fees_records':fees_records,'sudent_records':sudent_records})
    else:
        messages.warning(request, 'Payment mode')
        return redirect('fees_parent')
        
        

def payment_status(request):
    payment_key=PaymentKeys.objects.all().last()
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=(payment_key.razorpay_key_id, payment_key.razorpay_key_secret))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        # cold_coffee = ColdCoffee.objects.get(order_id=response['razorpay_order_id'])
        # cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
        # cold_coffee.paid = True
        # cold_coffee.save()
        return render(request, 'payment/payment_status.html', {'status': True})
    except:
        return render(request, 'payment/payment_status.html', {'status': False})
    
