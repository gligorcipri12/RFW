from flask import Flask, request
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

RESPONSE_LOG_FILE = "responses_log.xlsx"

# Creare fișier log dacă nu există
if not os.path.exists(RESPONSE_LOG_FILE):
    pd.DataFrame(columns=["timestamp", "approval_id", "response", "user_email"]).to_excel(RESPONSE_LOG_FILE, index=False)

@app.route("/raport/aprobare")
def aprobare():
    approval_id_param = request.args.get("id", "")
    user_email = request.args.get("user", "").lower()
    response = request.args.get("response", "no_action")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df_log = pd.read_excel(RESPONSE_LOG_FILE)

    deja_votat = df_log[
        (df_log["approval_id"] == approval_id_param) &
        (df_log["user_email"].str.lower() == user_email)
    ]

    if not deja_votat.empty:
        return f"""
        <html><body>
        <h2>⚠️ Vot deja înregistrat</h2>
        <p>Ați răspuns deja la acest raport.</p>
        </body></html>
        """

    nou = pd.DataFrame([{
        "timestamp": timestamp,
        "approval_id": approval_id_param,
        "response": response,
        "user_email": user_email
    }])
    df_log = pd.concat([df_log, nou], ignore_index=True)
    df_log.to_excel(RESPONSE_LOG_FILE, index=False)

    return f"""
    <html><body>
    <h2>✅ Răspuns înregistrat</h2>
    <p><b>Raport ID:</b> {approval_id_param}</p>
    <p><b>Răspuns:</b> {response}</p>
    <p><b>Utilizator:</b> {user_email}</p>
    <p><b>Data:</b> {timestamp}</p>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
