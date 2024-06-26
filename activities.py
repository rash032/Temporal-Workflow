from temporalio import activity
import requests

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
    response = requests.post("http://localhost:3333/payment", json={ "txn_amount": details.amount,"credit_account_id": details.account_id})
    print(response.json())

    return response.json()