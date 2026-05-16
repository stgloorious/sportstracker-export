#!/bin/env python3
#
# SPDX-Copyright-Text: Copyright (c) 2026 Stefan Gloor
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Use the Sports Tracker API to download all GPX files"""

import os
import json
import logging

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_session_key(path: str = "secret.txt") -> str:
    """Read the session key from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


class SportsTrackerAPI:
    """Abstraction for the Sports Tracker API."""
    base_url = 'https://api.sports-tracker.com'

    def __init__(self, session_key: str):
        """
        Set up connection and session.

        Sports Tracker uses a custom header for authentication.
        """
        self.session = requests.Session()
        self.session.headers.update({"Sttauthorization": session_key})

    def get_workouts(self, limit: int = 10000):
        """ Get a list of workouts. """
        resource = f'/apiserver/v1/workouts?limited=true&limit={limit}'
        response = self.session.get(self.base_url + resource)
        data = json.loads(response.text)
        if data['error'] is not None:
            raise RuntimeError(f"API error: {data['error']}")
        return data['payload']

    def download_gpx(self, workout_key: str):
        """Download GPX data for a workout."""
        resource = f'/apiserver/v1/workout/exportGpx/{workout_key}'
        resource += f'?token={self.session.headers["Sttauthorization"]}'
        response = self.session.get(self.base_url + resource)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to download GPX for workout {workout_key}")
        return response.content


def save_gpx(workout_key: str, gpx_data: bytes):
    """Save GPX data to a file."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_dir, '..', 'export', f"{workout_key}.gpx")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(gpx_data)
    logger.info("Saved GPX for workout %s to %s", workout_key, filename)

def main():
    """Download all workouts from Sports Tracker and save as GPX files."""
    session_key = read_session_key("secret.txt")
    api = SportsTrackerAPI(session_key)

    workouts = api.get_workouts()
    logger.info("Found %d workouts", len(workouts))
    for workout in workouts:
        workout_key = workout['workoutKey']
        gpx_data = api.download_gpx(workout_key)
        save_gpx(workout_key, gpx_data)

if __name__ == "__main__":
    main()
