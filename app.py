# -*- coding: utf-8 -*-
from flask import Flask, request, Response, render_template
import datetime
import requests
import os
from requests.auth import HTTPBasicAuth
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/sendfax")
def sendfax():
    to = request.args.get('to') or os.environ['TO']
    if (to[:1] == '0'):
        to = '+81'+to[1:]
    pdf = request.args.get('pdf') or 'sample.pdf'
    url = "https://fax.twilio.com/v1/Faxes"
    host = request.headers['HOST']
    accountSid = os.environ['ACCOUNT_SID']
    authToken = os.environ['AUTH_TOKEN']
    mediaUrl = 'http://'+host+'/static/'+pdf
    r = requests.post(url, data={
        "From": os.environ['FROM'],
        "To": to,
        "MediaUrl": mediaUrl
    }, auth=HTTPBasicAuth(accountSid, authToken))
    print(r.status_code)
    print(r.json())

    return 'FAX('+pdf+') sent to '+to+'.'

# FAXを受信したときにTwilioから呼ばれるWebHook
@app.route("/receive", methods=['POST'])
def receive():
    # パラメータを表示
    for k, v in request.form.items():
        print(k, v)

    # FAXを受信
    twiml = '<?xml version="1.0" encoding="UTF-8"?>'
    twiml += '<Response>'
    twiml += '<Receive action="/actionReceiver" method="POST" />'
    twiml += '</Response>'
    return Response(twiml, mimetype='text/xml')

# <Receive>動詞で指定したAction URL
@app.route('/actionReceiver', methods=['POST'])
def actionReceiver():
    # パラメータを表示
    for k, v in request.form.items():
        print(k, v)

    # ステータスが受信完了
    if (request.form["FaxStatus"] == 'received'):
        # 受信日時
        receivedDate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 送信元
        from_ = request.form["From"]
        from_ = from_.replace('+81', '0')   # 日本用
        from_ = from_.replace('+1', '0')    # US用
        # FAXをダウンロード
        mediaUrl = request.form["MediaUrl"]
        filename = download_file(mediaUrl, receivedDate, from_)
        print(filename, 'Downloaded.')

    return 'OK'

# FAXダウンロード
def download_file(mediaUrl, receivedDate, from_):
    # FAXディレクトリに、送信元_受信日時.pdfという名前で保存
    filename = './FAX/'+from_+'_'+receivedDate+'.pdf'
    r = requests.get(mediaUrl, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename


if __name__ == "__main__":
    app.run(port=3000, debug=True)
