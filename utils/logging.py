"""
The log_request function logs HTTP requests in a Flask application, extracting and printing relevant information
such as timestamp, status code, client IP, request method, URL, headers, JSON data, and query parameters.
It uses the Colorama library for color-coded output.
"""

import time
import math
import colorama
import flask


def log_request(response: flask.Response, request: flask.Request):
    try:
        payload_len = len(request.json)
    except:
        payload_len = 0

    # if payload can not be found payload is set to an empty dict.
    # Else werkzeug.extension.UnsupportedMediaType might be raised

    status_colors = {
        100: [colorama.Back.YELLOW, colorama.Fore.YELLOW],
        200: [colorama.Back.LIGHTGREEN_EX, colorama.Fore.LIGHTGREEN_EX],
        300: [colorama.Back.GREEN, colorama.Fore.GREEN],
        400: [colorama.Back.LIGHTMAGENTA_EX, colorama.Fore.LIGHTMAGENTA_EX],
        500: [colorama.Back.RED, colorama.Fore.RED]
    }

    additional_message = ""

    if response.headers.get("error"):
        additional_message = colorama.Style.DIM + "\"" + status_colors[math.floor(response.status_code/100)*100][1] + \
                             response.headers.get("error") + colorama.Fore.RESET + "\"" + colorama.Style.RESET_ALL
    # If the server send an error it will be displayed too for debugging reasons

    print(colorama.Fore.LIGHTBLACK_EX, time.strftime("[%H:%M:%S %d/%b/%Y]"), colorama.Style.RESET_ALL,
          # showing current date and time
          colorama.Fore.BLACK, status_colors[math.floor(response.status_code/100)*100][0], response.status_code,
          colorama.Style.RESET_ALL,
          # rounding down to the nearest hundredth to get the status code category and then its color
          colorama.Fore.BLACK + colorama.Back.WHITE, request.remote_addr, colorama.Style.RESET_ALL,
          # client ip
          colorama.Fore.LIGHTBLACK_EX, request.method, request.url, f"HEADERS:{len(request.headers)}",
          f"JSON:{payload_len}", f"ARGS:{len(request.args)}", colorama.Style.RESET_ALL,
          # request informations
          additional_message
          )
