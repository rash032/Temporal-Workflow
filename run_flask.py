import asyncio

from flask import Flask, current_app, jsonify, make_response, request
from temporalio.client import Client

from run_worker import SendEmailWorkflow
from shared_objects import WorkflowOptions, task_queue_name

app = Flask(__name__)


async def connect_temporal(app):
    client = await Client.connect("localhost:7233")
    app.temporal_client = client


def get_client() -> Client:
    return current_app.temporal_client

@app.route("/subscribe", methods=["POST"])
async def start_subscription():
    client = get_client()

    email: str = str(request.json.get("email"))
    data: WorkflowOptions = WorkflowOptions(email=email)
    await client.start_workflow(
        SendEmailWorkflow.run,
        data,
        id=data.email,
        task_queue=task_queue_name,
    )

    message = jsonify({"message": "Resource created successfully"})
    response = make_response(message, 201)
    return response

if __name__ == "__main__":
    # Create Temporal connection.
    asyncio.run(connect_temporal(app))

    # Start API
    app.run(debug=True)