#モジュールのインポート
import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


#エンコードの指定
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)


#自身のアカウント名とアプリ パスワード
MY_GMAIL_ACCOUNT = ""
MY_GMAIL_PASSWORD = ""
#送信先のアドレスと宛名
TO_ADDRESS = ""
SEND_TO = ""
#日付を設定
TODAY_DATE = datetime.date.today()
DELIVERY_DATE = TODAY_DATE + datetime.timedelta(days=7)
#件名と本文(html形式)の設定
SUBJECT = "{0}様、{1}分の発注書をお送りします。".format(SEND_TO,TODAY_DATE)
BODY = "表題の発注書をお送りします。<br>添付ファイルをご確認ください。<br>本発注の納期は{0}となります。<br><br>株式会社".format(DELIVERY_DATE)
#添付ファイル(pdf)
FILENAME = ""


def create_message(from_addr, to_addr, subject, body):

  #メールの作成
  msg = MIMEMultipart()
  msg["Subject"] = subject
  msg["To"] = to_addr
  msg["From"] = from_addr
  msg_body = MIMEText(body,"html")
  msg.attach(msg_body)

  #添付ファイルの設定
  filename = FILENAME
  file = open(filename, "rb")
  attachment_file = MIMEBase("application", 'pdf')
  attachment_file.set_payload((file).read())
  file.close()
  encoders.encode_base64(attachment_file)
  attachment_file.add_header("Content-Disposition", "attachment", filename=filename)
  msg.attach(attachment_file)

  return msg




def send_message(msg):
  server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
  server.login(MY_GMAIL_ACCOUNT, MY_GMAIL_PASSWORD)
  server.send_message(msg)
  server.close()
  print("送信完了")


if __name__ == '__main__':
  #メールの送信
  msg = create_message(MY_GMAIL_ACCOUNT, TO_ADDRESS, SUBJECT, BODY)
  send_message(msg)
