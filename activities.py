from temporalio import activity
import requests
from decimal import Decimal

from shared_objects import EmailDetails, PaymentDetails


@activity.defn
async def send_email(details: EmailDetails) -> str:
    print(
        f"Sending email to {details.email} with message: {details.message}, count: {details.count}"
    )
    return "success"

@activity.defn
async def post_payment(details: PaymentDetails) -> dict:
    print(
        f"Paying {details.amount} via paytm"
    )
    response = requests.post("http://localhost:3333/payment", json={"txn_amount": str(details.amount),"credit_account_id": details.account_id})
    print(response.json())

    return response.json()

@activity.defn
async def account_2_account_credit(payment_confirmation_data: dict) -> dict:
    print("payment_confirmation_data", payment_confirmation_data)
    print(
        f"Crediting to account_id"
    )
    response = requests.post("http://localhost:3331/credit", json={"txn_amount": str(payment_confirmation_data.get("txn_amount")),"credit_account_id": payment_confirmation_data.get("account_id")})
    print(response.json())

    return response.json()