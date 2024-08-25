import threading
import time

import requests
from flask import request
from playwright.sync_api import sync_playwright

from app import app


def start_flask_app():
    app.run(port=5000)


def stop_flask_app():
    requests.get('http://localhost:5000/shutdown')


# Add this function to your app.py
def add_shutdown_route(app):
    @app.route('/shutdown')
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return 'Server shutting down...'


def before_all(context):
    # Add shutdown route to the Flask app
    add_shutdown_route(app)

    # Start Flask app in a separate thread
    context.flask_thread = threading.Thread(target=start_flask_app)
    context.flask_thread.daemon = True  # Set thread as daemon
    context.flask_thread.start()

    # Wait for the Flask app to start
    for i in range(10):  # Try for 5 seconds
        try:
            requests.get('http://localhost:5000')
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        raise Exception("Flask app failed to start")

    # Set up Playwright
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)  # Set to False for debugging
    context.page = context.browser.new_page()


def after_all(context):
    # Clean up Playwright
    context.page.close()
    context.browser.close()
    context.playwright.stop()

    # Shut down Flask app
    stop_flask_app()
    context.flask_thread.join(timeout=5)  # Wait for the thread to finish

    # If the thread is still alive, we'll need to forcefully terminate it
    if context.flask_thread.is_alive():
        print("Warning: Flask thread did not shut down gracefully")


def before_scenario(context, scenario):
    # Navigate to the homepage before each scenario
    context.page.goto('http://localhost:5000')
    print(f"Starting scenario: {scenario.name}")


def after_scenario(context, scenario):
    # Clear cookies and local storage after each scenario
    context.page.evaluate("() => { localStorage.clear(); }")
    context.page.context.clear_cookies()

    if scenario.status == "failed":
        # Take a screenshot on failure
        context.page.screenshot(path=f"failure_{scenario.name.replace(' ', '_')}.png")
        print(f"Scenario failed: {scenario.name}")
        print(f"Page URL: {context.page.url}")
        print(f"Page content: {context.page.content()}")
