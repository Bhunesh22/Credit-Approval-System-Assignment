from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from .serializers import CustomerSerializer
from .serializers import LoanSerializer
from datetime import datetime
from datetime import date
import time
import random
from dateutil.relativedelta import relativedelta

@api_view(['POST'])
def register_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Perform additional logic if needed before saving
            monthly_income = serializer.validated_data['monthly_salary']
            serializer.validated_data['approved_limit'] = round(36 * monthly_income, -5)

            serializer.save()

            response_data = {
                "customer_id": serializer.data['id'],
                "first_name": serializer.data['first_name'],
                "last_name": serializer.data['last_name'],
                "age": serializer.data['age'],
                "phone_number": serializer.data['phone_number'],
                "monthly_salary": serializer.data['monthly_salary'],
                "approved_limit": serializer.data['approved_limit']
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def check_eligibility(request):
    if request.method == 'POST':
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        credit_score = calculate_credit_score(customer)
        print("credit_score", credit_score)

        if credit_score > 50:
            approved_loan = True
            corrected_interest_rate = interest_rate
        elif 30 < credit_score <= 50:
            approved_loan = True
            corrected_interest_rate = max(interest_rate, 12)
        elif 10 < credit_score <= 30:
            approved_loan = True
            corrected_interest_rate = max(interest_rate, 16)
        else:
            approved_loan = False
            corrected_interest_rate = None

        response_data = {
            'customer_id': customer_id,
            'approval': approved_loan,
            'interest_rate': interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment(loan_amount, corrected_interest_rate, tenure),
        }

        return Response(response_data, status=status.HTTP_200_OK)


def calculate_credit_score(customer):

    loans_of_customer = Loan.objects.filter(customer_id=customer.id)

    if len(loans_of_customer) == 0 :
        print("loans_of_customer", len(loans_of_customer))
        return 0

    number_of_past_loans = len(loans_of_customer)
    past_loans_paid_on_time = 0
    total_past_loans_emis = 0
    loan_approved_volume = 0
    sum_current_loans = 0
    no_of_currently_active_loan = 0
    current_monthly_emis = 0


    for loan in loans_of_customer:
        past_loans_paid_on_time += loan.emis_paid_on_time

        total_past_loans_emis += loan.tenure

        loan_approved_volume += loan.loan_amount

        current_date = time.strptime(str(date.today()), '%Y-%m-%d')
        end_date = time.strptime(str(loan.end_date), '%Y-%m-%d')

        if end_date > current_date:

            sum_current_loans += loan.loan_amount

            no_of_currently_active_loan += 1

            current_monthly_emis += loan.monthly_installment


    payment_on_time_percent = (past_loans_paid_on_time/total_past_loans_emis)*100

    percent_of_loan_approved_volume_in_ten_lakhs = (loan_approved_volume/1000000)*100


    approved_limit = customer.approved_limit
    if sum_current_loans > approved_limit:
        return 0

    if current_monthly_emis > 0.5 * customer.monthly_salary:
        return 0

    print("payment_on_time_percent", payment_on_time_percent)
    print("percent_of_loan_approved_volume_in_ten_lakhs", percent_of_loan_approved_volume_in_ten_lakhs)
    print("number_of_past_loans", number_of_past_loans)
    print("no_of_currently_active_loan", no_of_currently_active_loan)
    weight_payment_on_time_percent = 0.35
    weight_loan_approved_volume = 0.2
    score_per_past_loans = 5  # Maximum 25 so it holds 0.25 weight
    score_per_currently_active_loan = 5 # Maximum 20 so it holds 0.2 weight

    credit_score = (
        weight_payment_on_time_percent*payment_on_time_percent +
        min(weight_loan_approved_volume*percent_of_loan_approved_volume_in_ten_lakhs, 20) +
        min(number_of_past_loans, 5)*score_per_past_loans +
        min(no_of_currently_active_loan, 4)*score_per_currently_active_loan
    )

    return int(credit_score)


def monthly_installment(loan_amount, corrected_interest_rate, tenure):

    if corrected_interest_rate is None:
        return None

    P = loan_amount
    R = (corrected_interest_rate/12)/100
    N = tenure
    installment = ((P*R)*((1 + R)**N))/((1 + R)**N - 1)

    return int(installment)


@api_view(['POST'])
def create_loan(request):
    if request.method == 'POST':
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)


        credit_score = calculate_credit_score(customer)

        if credit_score > 50:
            approved_loan = True
            corrected_interest_rate = interest_rate
        elif 30 < credit_score <= 50:
            approved_loan = True
            corrected_interest_rate = max(interest_rate, 12)
        elif 10 < credit_score <= 30:
            approved_loan = True
            corrected_interest_rate = max(interest_rate, 16)
        else:
            approved_loan = False
            corrected_interest_rate = None


        if approved_loan == False:
            return Response({'error': 'Loan not approved due to your low credit score'}, status=status.HTTP_400_BAD_REQUEST)

        loan_data = {
            'customer_id': customer_id,
            'loan_id': random.randint(10000, 99999),
            'loan_amount': loan_amount,
            'interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment(loan_amount, corrected_interest_rate, tenure),
            'start_date': date.today(),
            'end_date': date.today() + relativedelta(months=tenure)
        }

        loan_serializer = LoanSerializer(data=loan_data)
        if loan_serializer.is_valid():
            loan_serializer.save()
            loan_data = {
                'customer_id': customer_id,
                'loan_id': loan_serializer.data['loan_id'],
                'loan_approved': approved_loan,
                'monthly_installment': loan_serializer.data['monthly_installment']
            }
            return Response(loan_data, status=status.HTTP_201_CREATED)

        return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    customer_serializer = CustomerSerializer(loan.customer_id)

    customer_data = {
        "id": customer_serializer.data['id'],
        "first_name": customer_serializer.data['first_name'],
        "last_name": customer_serializer.data['last_name'],
        "age": customer_serializer.data['age'],
        "phone_number": customer_serializer.data['phone_number']
    }

    response_data = {
        'loan_id': loan_id,
        'customer': customer_data,
        'loan_amount': loan.loan_amount,
        'interest_rate': loan.interest_rate,
        'monthly_installment': loan.monthly_installment,
        'tenure': loan.tenure,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_loans(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer_id=customer_id)

    data = []
    for loan_data in loans:
        emis_left = 0
        loan = {}

        current_date = time.strptime(str(date.today()), '%Y-%m-%d')
        end_date = time.strptime(str(loan_data.end_date), '%Y-%m-%d')
        if end_date > current_date:
            emis_left = (loan_data.end_date.year - date.today().year) * 12 + loan_data.end_date.month - date.today().month
        loan['loan_id'] = loan_data.loan_id
        loan['loan_amount'] = loan_data.loan_amount
        loan['interest_rate'] = loan_data.interest_rate
        loan['monthly_installment'] = loan_data.monthly_installment
        loan['repayments_left'] = emis_left
        data.append(loan)

    return Response(data, status=status.HTTP_200_OK)
