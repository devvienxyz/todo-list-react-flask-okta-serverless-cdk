# import asyncio
# import json
# from authlib.integrations.flask_oauth2 import current_token
# from flask import g, session
# from application import api, oidc

# loop = asyncio.get_event_loop()




# @api.route("/login")
# @oidc.require_login
# @oidc.accept_token(scopes=["openid", "profile", "email", "phone"])
# def login():
#     # return "Welcome %s" % session["oidc_auth_profile"].get("email")
#     profile = g._oidc_auth.userinfo(token=current_token)
#     return json.dumps(f'Welcome {profile["fullname"]}')


# @api.route("/logout", methods=["POST"])
# @oidc.require_login
# @oidc.accept_token(scopes=["profile"])
# def logout():
#     oidc.logout()
#     return "", 200
