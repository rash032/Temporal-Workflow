import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import send_email, post_payment
from shared_objects import task_queue_name
from workflow import SendEmailWorkflow, PaymentWorkflow


async def main():
    client = await Client.connect("0.0.0.0:7233", namespace="default")

    worker = Worker(
        client,
        task_queue="payment",
        workflows=[PaymentWorkflow],
        activities=[post_payment],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())