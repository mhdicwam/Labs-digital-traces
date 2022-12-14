from flask import Flask, redirect, url_for, render_template, request, flash
import logging
import requests
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os 
"""A simple example of how to access the Google Analytics API."""


root_dir = os.path.dirname(os.path.abspath(__file__))

# from flask_analytics import Analytics

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)



URL = "https://ttq8wo.deta.dev/"

SCOPES = 'https://www.googleapis.com/auth/analytics.readonly'
KEY_FILE_LOCATION = os.path.join(root_dir,'monitor-visitors-746310e7baa0.json')
VIEW_ID = '282228495'  # You can find this in Google Analytics > Admin > Property > View > View Settings (VIEW ID)



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

    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251023329-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251023329-1');
    </script>
    """
    return prefix_google + render_template("index.html")


@app.route('/logger', methods=["GET", "POST"])
def logger():

    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251023329-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251023329-1');
    </script>
    """
    app.logger.debug('This is a debug message')
    print("this a debug message in python")
    value = request.form.get('log_input')
    print(value)
    app.logger.info('%s displayed successfully', value)
    return prefix_google + render_template("logger.html", text=value)


@app.route('/cookies', methods=["GET", "POST"])
def get_cookies():
    req = requests.get(
            "https://analytics.google.com/analytics/web/#/p345114172/reports/reportinghub?params=_u..nav%3Dmaui"
    )
    return req.cookies.get_dict()




@app.route('/visitors', methods=["GET", "POST"])
def get_number_visitors():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    visitors = get_visitors(response)

    print(visitors)
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251023329-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251023329-1');
    </script>
    """
    return prefix_google + render_template('visitors.html', visitors=str(visitors))



@app.route('/trend', methods=["GET", "POST"])
def google_trend():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251023329-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251023329-1');
    </script>
    """
    from pytrends.request import TrendReq
    from datetime import date


    pytrend = TrendReq()


    kw_list = ["chine","sintomas covid"]
    pytrend.build_payload(kw_list=kw_list,timeframe=f'2022-10-26 {date.today()}', geo='BR')

 
    # Interest Over Time
    trend_data=pytrend.interest_over_time()
    
    print(trend_data)
    print(trend_data.chine)
    print(trend_data["sintomas covid"])
    return prefix_google + render_template('trends.html',trend=trend_data)

if __name__ == '__main__':
    app.run(debug=True)
