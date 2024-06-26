from dataclasses import dataclass
from decimal import Decimal

task_queue_name = "email_subscription"


@dataclass
class WorkflowOptions:
    email: str


@dataclass
class EmailDetails:
    email: str = ""
    message: str = ""
    count: int = 0
    subscribed: bool = False

@dataclass
class PaymentDetails:
    account_id: str = ""
    type: str = ""
    amount: Decimal = 0.00