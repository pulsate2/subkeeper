import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from typing import Optional
from datetime import datetime, timedelta, timezone
import os

class Notifier:
    def __init__(self, db_session):
        self.db = db_session
        self._load_config()
    
    def _load_config(self):
        from .models import Settings
        
        smtp = self.db.query(Settings).filter(Settings.key == "smtp_conf").first()
        wechat = self.db.query(Settings).filter(Settings.key == "wechat_conf").first()
        webhook = self.db.query(Settings).filter(Settings.key == "webhook_conf").first()
        
        self.smtp_config = json.loads(smtp.value) if smtp else None
        self.wechat_config = json.loads(wechat.value) if wechat else None
        self.webhook_config = json.loads(webhook.value) if webhook and webhook.value else {"webhook_key": ""}
    
    def send_email(self, subject: str, body: str) -> bool:
        if not self.smtp_config:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config.get('from')
            msg['To'] = self.smtp_config.get('to')
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            with smtplib.SMTP(self.smtp_config.get('host'), self.smtp_config.get('port')) as server:
                if self.smtp_config.get('use_tls'):
                    server.starttls()
                server.login(self.smtp_config.get('username'), self.smtp_config.get('password'))
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
    
    def send_wechat(self, title: str, content: str) -> bool:
        if not self.wechat_config:
            return False
        
        try:
            token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.wechat_config.get('corpid')}&corpsecret={self.wechat_config.get('secret')}"
            token_resp = requests.get(token_url)
            access_token = token_resp.json().get('access_token')
            
            if not access_token:
                return False
            
            send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            message = {
                "touser": self.wechat_config.get('touser', '@all'),
                "msgtype": "text",
                "agentid": self.wechat_config.get('agentid'),
                "text": {
                    "content": f"{title}\n\n{content}"
                }
            }
            
            resp = requests.post(send_url, json=message)
            return resp.json().get('errcode') == 0
        except Exception as e:
            print(f"WeChat send failed: {e}")
            return False
    
    def send_notification(self, title: str, content: str, notify_email: bool = True, notify_wechat: bool = True, notify_webhook: bool = True):
        """发送通知 - 支持邮件、企业微信和 Webhook，可根据偏好开关"""
        # 发送邮件
        if notify_email:
            self.send_email(title, content)
        # 发送企业微信
        if notify_wechat:
            self.send_wechat(title, content)
        # 发送 Webhook 通知
        if notify_webhook:
            self.send_webhook_notification(title, content)

    def send_webhook_notification(self, title: str, content: str):
        """发送通知到企业微信 Webhook"""
        webhook_key = self.webhook_config.get('webhook_key', '') if self.webhook_config else ''
        
        if not webhook_key:
            print('⚠️ 未配置企业微信 Webhook Key，跳过发送通知')
            return

        # 获取并格式化香港时间
        hkt = timezone(timedelta(hours=8), 'HKT')
        hkt_time_str = datetime.now(hkt).strftime('%Y-%m-%d %H:%M:%S %Z')
        
        full_message = f"{title}\n\n{content}"
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        payload = {
            "msgtype": "text",
            "text": {
                "content": full_message
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status() # 如果请求失败 (例如 4xx 或 5xx)，则会抛出异常
            print('✅ 企业微信 Webhook 通知发送成功')
        except requests.RequestException as e:
            print(f'⚠️ 企业微信 Webhook 通知发送失败: {e}')