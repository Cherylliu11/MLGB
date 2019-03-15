from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from MLGB.settings import EMAIL_FROM

def random_str(randomlength=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type='register'):
    email_record=EmailVerifyRecord()
    code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title=''
    email_body=''

    if send_type=='register':
        email_title='mmp披萨店注册激活链接'
        email_body='请点击下面的链接激活你的账号：http://106.14.180.113/active/{0}'.format(code)

        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type=='forget':
        email_title = 'mmp披萨店密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://106.14.180.113/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass