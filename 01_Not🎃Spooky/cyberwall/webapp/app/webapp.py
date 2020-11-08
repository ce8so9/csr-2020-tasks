from flask import redirect, Flask, render_template, request, abort
from flask import url_for, send_from_directory, make_response, Response
from subprocess import check_output


app = Flask(__name__)


mgmt_templates = {
    "overview": "overview.html",
    "debug": "debug.html",
    "blockchain": "blockchain.html",
    "cloudprotect": "cloud.html",
    "ai": "ai.html",
}


@app.route('/static/<path:p>')
def wtf(p):
    return send_from_directory("static", p)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/management.html", methods=["GET", "POST"])
def management():
    page = request.args.get("page", "overview")
    try:
        template = mgmt_templates[page]
    except KeyError:
        return "Page does not exist."
    
    if request.method == "POST" and page == "debug":
        target = request.form["target"]
        out = check_output(f"ping -c 1 {target}", shell=True).decode()
        return render_template(template, output=out)

    return render_template(template)


if __name__ == '__main__':
    app.run()
