import os
import json
import pytest

from src.app import flask_app
from src.payloads.home import MODAL_REQUEST

from tests.utils.mock_request import mock_event_handler, mock_base_client
from tests.fixtures.change_request import (
    OPEN_APP_HOME_FIX1,
    build_request_view,
    build_request_message_view,
    build_static_select_action_value,
    build_buttom_action_value,
    build_text_state_value,
    build_static_select_state_value
)

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_open_app_home(client):
    response = client.post(f"/slack/events", json = OPEN_APP_HOME_FIX1)
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_open_change_request_modal(client):
    response = client.post(
        f"/slack/events", json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "request_change",
                text = "Request Change"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_evironment(client):
    response = client.post(
        f"/slack/events", json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_environment",
                text = "Production",
                value = "default"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_group(client):
    response = client.post(
        f"/slack/events", json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_group",
                text = "Release 1",
                value = "Release 1"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_switcher(client):
    response = client.post(
        f"/slack/events", json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_switcher",
                text = "MY_FEATURE",
                value = "MY_FEATURE"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_status(client):
    response = client.post(
        f"/slack/events", json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_status",
                text = "Activate",
                value = "true"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_submit_for_review(client):
    response = client.post(
        f"/slack/events", json = build_request_view(
            req_type = "view_submission",
            callback_id = "change_request_review",
            state_fixture = {
                **build_static_select_state_value(
                    action_id = "selection_environment",
                    text = "Production",
                    value = "default"
                ),
                **build_static_select_state_value(
                    action_id = "selection_group",
                    text = "Release 1",
                    value = "Release 1"
                ),
                **build_static_select_state_value(
                    action_id = "selection_switcher",
                    text = "MY_FEATURE",
                    value = "MY_FEATURE"
                ),
                **build_static_select_state_value(
                    action_id = "selection_status",
                    text = "Activate",
                    value = "true"
                )
            }
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_submit_request(client):
    private_metadata = json.dumps({
        "environment": "default",
        "environment_alias": "Production",
        "group": "Release 1",
        "switcher": "MY_FEATURE1",
        "status": bool(True)
    })

    response = client.post(
        f"/slack/events", json = build_request_view(
            private_metadata = private_metadata,
            actions_fixture = build_static_select_action_value(
                action_id = "change_request_submit",
                text = "Submit"
            ),
            state_fixture = build_text_state_value(
                action_id = "selection_observation",
                value = "My observation here"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_approve_request(client):
    response = client.post(
        f"/slack/events", json = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_approved",
                text = "Approve",
                value = "ticket_123"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_deny_request(client):
    response = client.post(
        f"/slack/events", json = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_denied",
                text = "Deny",
                value = "ticket_123"
            )
        )
    )
    assert response.status_code == 200