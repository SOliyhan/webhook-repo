# Webhook

This repository demonstrates using GitHub webhooks to send events (Push, Pull Request, Merge) to an endpoint, storing them in MongoDB, and displaying them in a web UI.

## Run the Flask Application

    python app.py

## Usage

- **Endpoints**:
  - `/webhook`: Receives GitHub webhook events.
  - `/events`: Fetches the latest events from MongoDB.
  - `/`: Displays the events in the web UI.
