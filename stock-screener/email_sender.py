import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_email(signals):

    if len(signals) == 0:
        print("No Buy Signals")
        return

    body = """
    <html>
    <body>

    <h2>📈 Daily Stock Buy Signals</h2>

    <table border="1" cellpadding="8">

    <tr>
        <th>Stock</th>
        <th>Entry</th>
        <th>Stop Loss</th>
        <th>Target</th>
        <th>RSI</th>
    </tr>

    """

    for s in signals:

        body += f"""
        <tr>
            <td>{s['symbol']}</td>
            <td>{s['entry']}</td>
            <td>{s['stop_loss']}</td>
            <td>{s['target']}</td>
            <td>{s['rsi']}</td>
        </tr>
        """

    body += """
    </table>

    <br>

    <b>Strategy</b>

    <ul>
    <li>EMA20 > EMA50</li>
    <li>RSI between 55 and 70</li>
    <li>MACD Bullish</li>
    <li>Volume Spike</li>
    </ul>

    </body>
    </html>
    """

    message = MIMEMultipart("alternative")

    message["Subject"] = "📈 Daily Buy Signals"

    message["From"] = EMAIL

    message["To"] = RECEIVER

    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(EMAIL, PASSWORD)

        server.send_message(message)

    print("Email Sent Successfully")
