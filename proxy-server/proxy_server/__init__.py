"""Entrypoint for proxy server """
__version__ = "0.1.0"
import datetime
import logging
import os

from flask import Flask, redirect, request
from flask.logging import create_logger
from markupsafe import escape

from proxy_server.database import DB


def create_app():
    """factory to create the app"""
    app = Flask(__name__)
    log = create_logger(app)
    log.setLevel(
        logging.INFO if os.getenv("APP_ENV") == "production" else logging.DEBUG
    )
    database = DB(log)

    @app.route("/vote/<username>")
    def vote_for_user(username):
        """Endpoint serves as a proxy to record the timestamp when the user has clicked the link to
        vote then redirects user

        Args:
            username (string): maplelegends username

        Returns:
            Response: redirect
        """
        user_agent = request.headers.get("User-Agent")
        log.info("user agent %s", user_agent)
        username = escape(username)
        log.info("user voted: %s", username)

        recorded_time = datetime.datetime.now(datetime.timezone.utc)
        result = database.get_timestamp_collection().insert_one(
            document={"timestamp": recorded_time, "username": username}
        )
        log.debug("Insertion ID: %s", result.inserted_id)

        return redirect(
            f"https://gtop100.com/topsites/MapleStory/sitedetails/MapleLegends-v62-Closed-Beta-87398?vote=1&pingUsername={username}",  # noqa: E501 pylint: disable=line-too-long
            code=302,
        )

    # TODO: add healthcheck endpoint

    return app
