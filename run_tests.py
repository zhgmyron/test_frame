import time, sys,os
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication

def run_report(test_dir):

    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')
    #
    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='Guest Manage System Interface Test Report',
                            description='Implementation Example with: ')
    runner.run(discover)
    fp.close()
    print(os.getcwd())


def report_file(test_dir):
    lists=os.listdir(test_dir)
    lists.sort(key=lambda fn:os.path.getmtime(test_dir+'\\'+fn))
    file_path= os.path.join(test_dir,lists[-1])
    return file_path

def send_email(newfile):
    f= open(newfile,'rb')
    mail_body = f.read()
    f.close()
    file_name= newfile.split('\\')[-1]
    time_now = time.strftime("%Y-%m-%d")

    datas= MIMEApplication(open(newfile,'rb').read())
    print(file_name)
    datas.add_header('Content-Disposition','attachment',filename=file_name)


    smtpserver = 'smtp.gmail.com'
    #发送邮箱用户名/密码
    user = 'zhgmyron@gmail.com'
    password='Asdfg1234567'
    #发送邮箱
    sender='zhgmyron@gmail.com'
    #多个接收邮箱，单个收件人的话，直接是receiver='XXX@126.com'
    receiver=['ron.zhao@pricerunner.com']
    cc= ['zhgmyron@gmail.com']
    #发送邮件主题
    subject = '测试报告'+ time_now

    message = MIMEMultipart('mixed')
    message['From'] = Header("Test team", 'utf-8')
    message['To'] =  Header(','.join(receiver), 'utf-8')
    message["CC"] =Header(','.join(cc), 'utf-8')
    #subject = 'Daily report'
    message['Subject'] = Header(subject, 'utf-8')
    msg_html1 = MIMEText(mail_body,'html','utf-8')

    message.attach(msg_html1)
    message.attach(datas)
    smtp=smtplib.SMTP(smtpserver,587)
    smtp.ehlo()
    smtp.starttls()
    #smtp.connect(smtpserver,587)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, message.as_string())
    print("email send successful")
    smtp.quit()
    # try:
    #     smtp=smtplib.SMTP(smtpserver,587)
    #     #smtp.connect(smtpserver,587)
    #     smtp.login(user, password)
    #     smtp.sendmail(sender, receiver, message.as_string())
    #     print("email send successful")
    #     smtp.quit()
    # except smtplib.SMTPException:
    #     print("Error: can't send emails")
if __name__ == "__main__":
    # test_data.init_data() # 初始化接口测试数据
    # # 指定测试用例为当前文件夹下的 interface 目录
    test_dir = './interface'
    run_report(test_dir)
    test_report_dir= '.\\report'
    new_report=report_file(test_report_dir)
    send_email(new_report)
    # print(report_file('.\\report'))