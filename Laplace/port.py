import os
from flask import Flask, request
import requests
from Laplace.Utility import db
from Laplace import bot
import asyncio

async def sendConfirmation(discordId: int, robloxId: int):
    user = await bot.bot.rest.fetch_user(discordId)
    userChannel = await user.fetch_dm_channel()
    await bot.bot.rest.create_message(userChannel.id, f"✅ Your roblox account has been linked to https://www.roblox.com/users/{robloxId}/profile")
         
async def sendFailure(discordId: int, robloxId: int):
    user = await bot.bot.rest.fetch_user(discordId)
    userChannel = await user.fetch_dm_channel()
    await bot.bot.rest.create_message(userChannel.id, f"❌ Your roblox account has failed to be linked to https://www.roblox.com/users/{robloxId}/profile")
         

app = Flask(__name__)
port = int(os.getenv("PORT", 8080))

clientSecret = os.getenv("oauth2")
clientId = os.getenv("clientId")
redirectUri = "https://laplaceomg-190212166685.us-central1.run.app/redirect"
scope = "openid"

@app.route("/")
def home():
    return "omg"

@app.route("/redirect")
def redirect():
    code = request.args.get('code')
    state = request.args.get('state')

    if not code or not state:
        return "missing code or state", 400
    
    if not state in db.pending:
        return "Invalid or expired verification link", 400
    
    response = requests.post(
        "https://apis.roblox.com/oauth/v1/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": clientId,
            "client_secret": clientSecret,
            "redirect_uri": redirectUri
        }
    ).json()

    if not "access_token" in response:
        return "oops there was an error :3", 400
    accessToken = response["access_token"]

    newResponse = requests.get(
        "https://apis.roblox.com/oauth/v1/userinfo",
        headers={"Authorization": f"Bearer {accessToken}"}
    ).json()        

    robloxUserId = int(newResponse.get("sub"))
    discordUserId = db.pending[state]['discord']
    desiredRobloxUserId = db.pending[state]['roblox']

    del db.pending[state]

    if robloxUserId != desiredRobloxUserId:
        asyncio.run(sendFailure(discordUserId, robloxUserId))
        return "Error linking account, you provided and logged into two different roblox accounts.", 400


    asyncio.run(sendConfirmation(discordUserId, robloxUserId))
    db.link(robloxUserId, discordUserId)
    return "Your account has been successfully linked."

@app.route("/tos")
def tos():
    return """Last Updated: October 25, 2025

1. Acceptance

By using Laplace, you agree to these Terms of Service.

2. Bot Usage

You may only use this bot for legitimate purposes.

Misuse, abuse, or attempts to hack the bot are prohibited.

3. Account Linking

Linking your Discord account to Roblox is voluntary.

You are responsible for maintaining the security of your own accounts.

4. Data

By verifying your account, you consent to collection of Discord ID and Roblox ID.

See our Privacy Policy for details.

5. Disclaimers

The bot is provided “as-is.”

We are not responsible for any damages resulting from bot use.

We are not affiliated with Roblox or Discord.

6. Termination

We may revoke access for users who violate these Terms.

7. Changes

We may modify these Terms at any time. Continued use constitutes acceptance of changes."""

@app.route("/privacy")
def privacy():
    return """Last Updated: October 25, 2025

Laplace (“we”, “our”, “us”) respects your privacy. This Privacy Policy explains how we collect, use, and protect your information when you use our Discord bot.

1. Information We Collect

Discord ID: Used to identify your account for verification purposes.

Roblox ID & Username: Collected only when you verify your Roblox account via OAuth2.

Optional Data: Any information you voluntarily provide via bot commands (e.g., preferences, feedback).

2. How We Use Your Information

To verify your Roblox account ownership.

To provide and maintain bot functionality.

To prevent abuse and ensure security.

3. Data Sharing

We do not sell, rent, or share your personal data with third parties, except as required by law.

4. Data Retention

Verification data is stored until you request deletion or if the bot is discontinued.

You can request deletion of your data by contacting the bot owner.

5. Security

We implement reasonable technical measures to protect your data.

No system is 100% secure; we cannot guarantee complete security.

6. Children’s Privacy

This bot is not intended for children under 13.

7. Changes to this Policy

We may update this Privacy Policy. Updated versions will be posted here."""

def init():
    app.run(host="0.0.0.0", port=port)
