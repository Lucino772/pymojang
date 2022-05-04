import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request

import mojang
import mojang.exceptions

load_dotenv()

app = Flask(__name__)
auth_app = mojang.app(
    os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), "http://localhost:3000"
)


def _sess_to_json(sess):
    return {
        "name": sess.name,
        "uuid": sess.uuid,
        "is_legacy": sess.is_legacy,
        "is_demo": sess.is_demo,
        "names": [
            {"name": name[0], "changed_to_at": name[1]} for name in sess.names
        ],
        "skin": {
            "url": sess.skin.source if sess.skin else None,
            "variant": sess.skin.variant if sess.skin else None,
        },
        "cape": {"url": sess.cape.source if sess.cape else None},
        "created_at": sess.created_at,
        "can_change_name": sess.name_change_allowed,
    }


@app.route("/")
def index():
    if request.args.get("code", False):
        try:
            sess = auth_app.get_session(request.args["code"])
            return jsonify(_sess_to_json(sess))
        except mojang.exceptions.MicrosoftInvalidGrant:
            pass

    return redirect(auth_app.authorization_url)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
