from flask import Flask, redirect, url_for, render_template, request, flash
import logging
import requests
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# from flask_analytics import Analytics

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

URL = "https://ttq8wo.deta.dev/"

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '<THE JSON FILE>'
VIEW_ID = '<APP VIEW ID>'  # You can find this in Google Analytics > Admin > Property > View > View Settings (VIEW ID)


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            KEY_FILE_LOCATION, SCOPES
    )
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
    return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:pageviews'}],
                        'dimensions': []
                    }]
            }
    ).execute()


def get_visitors(response):
    visitors = 0  # in case there are no analytics available yet
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dateRangeValues = row.get('metrics', [])

            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    visitors = value

    return str(visitors)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")


@app.route('/logger', methods=["GET", "POST"])
def logger():
    app.logger.debug('This is a debug message')
    print("this a debug message in python")
    value = request.form.get('log_input')
    print(value)
    app.logger.info('%s displayed successfully', value)
    return render_template("logger.html", text=value)


@app.route('/cookies', methods=["GET", "POST"])
def get_cookies():
    req = requests.get(
            "https://analytics.google.com/analytics/web/#/p345114172/reports/reportinghub?params=_u..nav%3Dmaui"
    )

    return req.cookies.get_dict()


@app.route('/visitors', methods=["GET", "POST"])
def get_number_visitors():
    req = requests.get(
            "https://analytics.google.com/analytics/web/#/p345114172/reports/reportinghub?params=_u..nav%3Dmaui"
    )

    return req.text


if __name__ == '__main__':
    app.run(debug=True)
