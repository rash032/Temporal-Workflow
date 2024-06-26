import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import send_email, post_payment
    from shared_objects import EmailDetails, WorkflowOptions, PaymentDetails


@workflow.defn
class SendEmailWorkflow:
    def __init__(self) -> None:
        self.email_details = EmailDetails()

    @workflow.run
    async def run(self, data: WorkflowOptions) -> None:
        print("here212321")
        duration = 3600
        self.email_details.email = data.email
        self.email_details.message = "Welcome to our Subscription Workflow!"
        self.email_details.subscribed = True
        self.email_details.count = 0

        while self.email_details.subscribed:
            self.email_details.count += 1
            if self.email_details.count > 1:
                self.email_details.message = "Thank you for staying subscribed!"

            try:
                await workflow.execute_activity(
                    post_payment,
                    self.payment_details,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                await asyncio.sleep(duration)

            except asyncio.CancelledError as err:
                # Cancelled by the user. Send them a goodbye message.
                self.email_details.subscribed = False
                self.email_details.message = "Sorry to see you go"
                await workflow.execute_activity(
                    send_email,
                    self.email_details,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                # raise error so workflow shows as cancelled.
                raise err
            

@workflow.defn
class PaymentWorkflow:
    def __init__(self) -> None:
        self.payment_details = PaymentDetails()

    @workflow.run
    async def run(self, data: PaymentDetails) -> dict:
        print("here212321")
        self.payment_details.account_id = data.account_id
        self.payment_details.amount = data.amount
        self.payment_details.type = data.type

        try:
            return await workflow.execute_activity(
                post_payment,
                self.payment_details,
                start_to_close_timeout=timedelta(seconds=10),
            )

        except asyncio.CancelledError as err:
            raise err
            