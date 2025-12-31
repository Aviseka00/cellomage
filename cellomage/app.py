from flask import Flask, render_template, request
from database.mongo import mongo
from services.cellpose_service import analyze_image
from services.image_utils import save_image
from services.audit_service import log_event
import os
import cv2

app = Flask(__name__)
app.config.from_pyfile("config.py")
mongo.init_app(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULT_FOLDER"], exist_ok=True)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        view = request.form["view"]

        filename, img_path = save_image(image, app.config["UPLOAD_FOLDER"])

        result_img, count, confluency = analyze_image(img_path, view)

        out_dir = f"{app.config['RESULT_FOLDER']}/{view}"
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, filename)
        cv2.imwrite(out_path, result_img)

        log_event(
            action="IMAGE_ANALYSIS",
            image_name=filename,
            model_used="my_cells_v2",
            cell_count=count,
            confluency=confluency,
            view_mode=view,
            ip_address=request.remote_addr
        )

        return render_template(
            "result.html",
            image=f"{view}/{filename}",
            count=count,
            confluency=confluency
        )

    return render_template("upload.html")

@app.route("/audit")
def audit():
    logs = mongo.db.audit_logs.find().sort("timestamp", -1)
    return render_template("audit.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
