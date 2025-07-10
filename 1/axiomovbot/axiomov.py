"""
Axiomov: Система жалоб на мошенников v2.6
Автор: https://github.com/axiomov0
Дисклеймер: Этот бот предназначен исключительно для законного использования, такого как отправка жалоб на нарушения в Telegram с предоставлением доказательств. Автор не несет ответственности за неправомерное использование, включая спам, злоупотребление или нарушение правил платформ. Пользователь обязан соблюдать законы и правила Telegram, а также предоставлять достоверные доказательства. Используйте на свой риск.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from art import text2art
from colorama import init, Fore, Style
import time
import os
import sys
import platform
import getpass

init()

RECEIVERS = [
    "sms@telegram.org",
    "dmca@telegram.org",
    "abuse@telegram.org",
    "sticker@telegram.org",
    "stopca@telegram.org",
    "security@telegram.org"
]

REASONS = {
    "1": {
        "name": "Доксинг",
        "template": "User {target} is engaging in doxxing, exposing private information such as addresses, phone numbers, or personal data without consent. This violates privacy and poses a serious threat. Please investigate and take action."
    },
    "2": {
        "name": "Мошенничество",
        "template": "User {target} is involved in fraudulent activities, including scams, phishing, or financial deception. Evidence of their malicious actions is attached (if provided). Immediate action is required."
    },
    "3": {
        "name": "Распространение CP",
        "template": "User {target} is distributing illegal content (CP) in violation of laws and platform policies. This is a critical issue requiring urgent investigation and account suspension."
    },
    "4": {
        "name": "Спам",
        "template": "User {target} is flooding channels or groups with spam messages, disrupting user experience and violating platform rules. Please review and enforce appropriate measures."
    },
    "5": {
        "name": "Угрозы",
        "template": "User {target} is issuing threats of violence, harassment, or intimidation. This behavior creates an unsafe environment and requires immediate intervention."
    }
}

def display_banner():
    os_info = f"{platform.system()} {platform.release()}"
    print(Fore.RED + text2art("Axiomov", font="block") + Style.RESET_ALL)
    print(Fore.RED + "[*] AxiomovBot: Система жалоб на мошенников v2.6" + Style.RESET_ALL)
    print(Fore.RED + f"[!] Запущено на {os_info}. Режим скрытности активирован." + Style.RESET_ALL)
    print(Fore.RED + "[!] Цель: нейтрализация цифровых угроз." + Style.RESET_ALL)
    print()

def loading_animation():
    chars = "/—\\|"
    for _ in range(10):
        sys.stdout.write(Fore.RED + f"\r[*] Инициализация протокола Axiomov... {chars[_ % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
    print()

def send_complaint(sender_email, sender_password, target_user, reason_key, attachment_path=None, target_link=""):
    if not sender_password:
        print(Fore.RED + "[!] Ошибка: Пароль не введен!" + Style.RESET_ALL)
        return

    reason = REASONS[reason_key]["template"].format(target=target_user)
    try:
        print(Fore.RED + "[*] Подключение к ядру SMTP..." + Style.RESET_ALL)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for receiver_email in RECEIVERS:
            msg = MIMEMultipart()
            msg['Subject'] = f"[AxiomovBot] Жалоба на пользователя: {target_user}"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            body = f"Детали жалобы:\n\nЦель: {target_user}\nПричина: {REASONS[reason_key]['name']}\n"
            if target_link:
                body += f"Ссылка на профиль: {target_link}\n"
            body += f"\n{reason}\n\nОтправлено через AxiomovBot ({platform.system()} {platform.release()})"
            msg.attach(MIMEText(body, 'plain'))

            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                msg.attach(part)
                print(Fore.RED + f"[*] Прикреплен файл: {attachment_path}" + Style.RESET_ALL)

            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(Fore.RED + f"[+] Жалоба отправлена на {receiver_email}" + Style.RESET_ALL)
            time.sleep(0.5)

        server.quit()
        print(Fore.RED + "[+] Все жалобы успешно отправлены!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка: {str(e)}" + Style.RESET_ALL)

def main():
    display_banner()
    sender_email = input(Fore.RED + "Введите ваш email: " + Style.RESET_ALL)
    sender_password = getpass.getpass(Fore.RED + "Введите пароль (скрытый ввод): " + Style.RESET_ALL)
    print(Fore.RED + "=== Выберите причину жалобы ===" + Style.RESET_ALL)
    
    for key, value in REASONS.items():
        print(Fore.RED + f"[{key}] {value['name']}" + Style.RESET_ALL)
    
    reason_key = input(Fore.RED + "Выберите причину (1-5): " + Style.RESET_ALL)
    if reason_key not in REASONS:
        print(Fore.RED + "[!] Неверный выбор причины!" + Style.RESET_ALL)
        return
    
    target_user = input(Fore.RED + "Имя пользователя или ID цели: " + Style.RESET_ALL)
    target_link = input(Fore.RED + "Ссылка на профиль (например, t.me/username, или Enter, если нет): " + Style.RESET_ALL)
    attachment_path = input(Fore.RED + "Путь к файлу-доказательству (или Enter, если без файла): " + Style.RESET_ALL)

    print(Fore.RED + "\n=== Подтверждение данных цели ===" + Style.RESET_ALL)
    print(Fore.RED + f"От: {sender_email}" + Style.RESET_ALL)
    print(Fore.RED + f"Кому: {', '.join(RECEIVERS)}" + Style.RESET_ALL)
    print(Fore.RED + f"Цель: {target_user}" + Style.RESET_ALL)
    if target_link:
        print(Fore.RED + f"Ссылка: {target_link}" + Style.RESET_ALL)
    print(Fore.RED + f"Причина: {REASONS[reason_key]['name']}" + Style.RESET_ALL)
    if attachment_path:
        print(Fore.RED + f"Файл: {attachment_path}" + Style.RESET_ALL)
    
    confirm = input(Fore.RED + "\n[?] Запустить протокол жалоб? (y/n): " + Style.RESET_ALL).lower()
    
    if confirm == 'y':
        loading_animation()
        send_complaint(sender_email, sender_password, target_user, reason_key, attachment_path, target_link)
    else:
        print(Fore.RED + "[!] Операция прервана." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
