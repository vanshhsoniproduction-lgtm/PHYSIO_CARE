from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from appointments.models import Appointment
import razorpay

def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def payment_initiate(request, appointment_id):
    # Fetch appointment
    appt = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    
    # 1. Validation: Appointment must be marked COMPLETED by doctor
    if appt.status != 'COMPLETED':
        messages.error(request, "Payment is only available for completed sessions.")
        return redirect('appointments:home')
        
    # 2. Validation: Fee must be set
    if not appt.fee:
        messages.error(request, "Fee has not been calculated yet.")
        return redirect('appointments:home')
        
    # 3. Validation: Already Paid
    if appt.payment_status == 'PAID':
        messages.info(request, "This appointment is already paid.")
        return redirect('appointments:home')

    # Create Razorpay Order
    client = get_razorpay_client()
    order_amount = int(appt.fee * 100) # Amount in paise
    order_currency = 'INR'
    
    try:
        payment_order = client.order.create(dict(
            amount=order_amount,
            currency=order_currency,
            payment_capture=1
        ))
        
        # Save Order ID
        appt.razorpay_order_id = payment_order['id']
        appt.save()
        
        context = {
            'appointment': appt,
            'razorpay_order_id': payment_order['id'],
            'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
            'razorpay_amount': order_amount,
            'currency': order_currency,
            'callback_url': '/payments/verify/', # Points to payment_verify view below
            'patient': request.user.patient
        }
        return render(request, 'payments/process.html', context)
        
    except Exception as e:
        messages.error(request, f"Error initiating payment: {str(e)}")
        return redirect('appointments:home')

from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def payment_verify(request):
    """
    Callback URL for Razorpay to verify payment.
    Ensures that failures do not incorrectly mark payments as PAID.
    """
    if request.method == "POST":
        data = request.POST
        
        # 1. Basic Data Validation
        required_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
        if not all(field in data for field in required_fields):
            logger.error("Missing required fields in Razorpay callback data.")
            return render(request, 'payments/failed.html', {'error': "Invalid payment data received."})

        try:
            client = get_razorpay_client()
            
            # 2. Verify Signature
            params_dict = {
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            }
            
            # This raises razorpay.errors.SignatureVerificationError if invalid
            client.utility.verify_payment_signature(params_dict)
            
            # 3. Atomic Database Update
            with transaction.atomic():
                # Get the appointment. Use select_for_update to prevent race conditions.
                appt = Appointment.objects.select_for_update().get(razorpay_order_id=data['razorpay_order_id'])
                
                # Double check if it's already paid to prevent duplicate processing
                if appt.payment_status == 'PAID':
                    return render(request, 'payments/success.html')
                
                appt.payment_status = 'PAID'
                appt.razorpay_payment_id = data['razorpay_payment_id']
                appt.razorpay_signature = data['razorpay_signature']
                appt.save()
            
            return render(request, 'payments/success.html')
            
        except Appointment.DoesNotExist:
            logger.error(f"Appointment not found for order_id: {data.get('razorpay_order_id')}")
            return render(request, 'payments/failed.html', {'error': "Transaction record not found."})
            
        except razorpay.errors.SignatureVerificationError:
            logger.warning(f"Signature verification failed for order_id: {data.get('razorpay_order_id')}")
            # If signature fails, we DO NOT change status. It remains PENDING.
            return render(request, 'payments/failed.html', {'error': "Payment verification failed. Security breach suspected."})
            
        except Exception as e:
            logger.exception(f"Unexpected error during payment verification: {str(e)}")
            # For any other error, keep it pending and show a generic message.
            return render(request, 'payments/failed.html', {'error': "A technical error occurred. Please contact support if your amount was deducted."})
            
    return redirect('appointments:home')