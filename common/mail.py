# coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from common import config,logger


class Mail:
    """
        powered by Mr lerry
        at 2021-11-12
        用来获取配置并发送邮件
    """
    def __init__(self):
        # 把mail配置信息存放在列表
        self.mail_info = {}

        self.mail_info['from'] = config.config['mail']
        self.mail_info['username'] = config.config['mail']
        self.mail_info['hostname'] = 'smtp.' + config.config['mail'][
                                               config.config['mail'].rfind('@') + 1:config.config['mail'].__len__()]   #用获取的mail下标获取邮箱后缀名
        # 第三方客户端邮箱登录需要填写SMTP的授权码登录
        self.mail_info['password'] = config.config['pwd']

        # 接收人
        self.mail_info['to'] = str(config.config['mailto']).split(',')
        # 抄送人
        self.mail_info['cc'] = str(config.config['mailcopy']).split(',')
        # 邮件标题
        self.mail_info['mail_subject'] = config.config['mailtitle']
        self.mail_info['mail_encoding'] = config.config['mail_encoding']


    def send(self, text):
        # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587
        smtp = SMTP_SSL(self.mail_info['hostname'])
        smtp.set_debuglevel(0)

        ''' SMTP 'ehlo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        '''
        smtp.ehlo(self.mail_info['hostname'])
        smtp.login(self.mail_info['username'], self.mail_info['password'])

        msg = MIMEText(text, 'html', self.mail_info['mail_encoding'])
        msg['Subject'] = Header(self.mail_info['mail_subject'], self.mail_info['mail_encoding'])
        msg['from'] = self.mail_info['from']

        logger.info(self.mail_info)
        # print(text)
        msg['to'] = ','.join(self.mail_info['to'])
        msg['cc'] = ','.join(self.mail_info['cc'])
        receive = self.mail_info['to']
        receive += self.mail_info['cc']

        try:
            smtp.sendmail(self.mail_info['from'], receive, msg.as_string())
            smtp.quit()
            logger.info('邮件发送成功')
        except Exception as e:
            logger.error('邮件发送失败：')
            logger.exception(e)


if __name__ == '__main__':
    config.get_config('../lib/conf/conf.txt')
    mail = Mail()
    mail.send('11111111111')
