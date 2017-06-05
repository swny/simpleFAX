# Twilio Programmable FAX demo

## ToDo

### Step.1 example.env を .env に名変

```
$ mv example.env .env
```

### Step.2 .env を編集

- Twilio管理コンソールにログインし、 Account SID と Auth Token を調べます。
- .env ファイルの ACCOUNT_SID と AUTH_TOKEN を更新します。
- FROM は、Twilio管理コンソールで購入したFAXに対応した050番号をE.164形式で指定します。
- TO は、送信先のFAX番号を指定します。送信先はURLで指定することもできます。

### Step.3 環境変数を設定

```
$ source .env
```

※ Windowsユーザの方は、上記内容を参考に適宜ユーザ環境変数を設定してください。

### Step.4 使用するライブラリの準備

今回は以下の3つのライブラリを使用しますので、それぞれインストールします。

```
$ pip install flask
$ pip install datetime
$ pip install requests
```

### Step.5 アプリケーションの実行

```
$ python app.py
```

### Step.6 ngrokで公開

```
$ ngrok http 3000
```

### Step.7 FAX受信の設定

- Twilioの管理コンソールにログインします。
- 購入済みのFAXに対応した050番号を選択します。
- ACCEPT INCOMING を Faxes に変更します。
- CONFIGURE WITH を Webhooks, or TwiML Bins or Functions に変更します。
- A FAX COMES IN を Webhook にし、先程起動した ngrok の URL に /receive を加えたURLを記載します。
- 保存ボタンを押して、設定を保存します。

## 使い方

### FAX受信

- 先程設定した、購入済みの050番号に対してFAXを送信します。
- しばらくすると、ローカルのFAXフォルダにFAXが保存されます。

### FAX送信

- 送信したいPDFファイルを、ローカルのstaticフォルダに格納します。
- 以下のURLを使ってFAXを送信します。

*ngrokで表示されたURL*/sendfax?to=*送信先FAX番号を0から始まる形式で指定*&pdf=*staticフォルダに格納したPDFファイルの名前(例:sample.pdf)*

toを省略すると、環境変数の TO が利用されます。
pdfを省略すると、staticフォルダの中のsample.pdfが送信されます。
