# Sports Tracker GPX Export

![check](https://github.com/stgloorious/sportstracker-export/actions/workflows/pylint.yml/badge.svg)

Export your Sports Tracker workouts to `*.gpx` files to import them on other platforms (e.g., Strava).

## Use
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- Open a browser, go to [Sports Tracker](https://www.sports-tracker.com/login), and log in.
- Press F12 to open developer tools. Navigate to Cookies and copy your session key.

![docs/cookie.png](docs/cookie.png)

- Paste the session key into a file called `secret.txt` in this repository.
- Run `uv run src/sportstracker_export.py`.
- If successful, all your workouts are exported to `export/`.
