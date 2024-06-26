# @@@SNIPSTART python-project-template-run-workflow
import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from shared_objects import WorkflowOptions, PaymentDetails
from workflow import SendEmailWorkflow, PaymentWorkflow
from activities import send_email


async def main() -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("localhost:7233")

    data: PaymentDetails = PaymentDetails(
        amount=250,
        account_id="12345",
        type = "CREDIT"
    )
    # data: WorkflowOptions = WorkflowOptions(
    #    email="rashmi.sahu@junio.in"
    # )
    print(data.account_id)

    try:
        # result = await client.execute_workflow(
        #     MoneyTransfer.run,
        #     data,
        #     id="pay-invoice-701",
        #     task_queue=MONEY_TRANSFER_TASK_QUEUE_NAME,
        # )

        result = await client.execute_workflow(
            PaymentWorkflow.run,
            data,
            id=data.account_id,
            task_queue="payment",
        )

        print(result)

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
