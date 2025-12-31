from flask import Flask, render_template, request, send_from_directory
from database.mongo import mongo
from services.cellpose_service import analyze_image
from services.image_utils import save_image
from services.audit_service import log_event
import os

# --------------------------------
# Flask App Setup
# --------------------------------
app = Flask(__name__)
app.config.from_pyfile("config.py")
mongo.init_app(app)

# --------------------------------
# Ensure required folders exist
# --------------------------------
UPLOAD_DIR = app.config["UPLOAD_FOLDER"]
RESULT_DIR = app.config["RESULT_FOLDER"]

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(os.path.join(RESULT_DIR, "dots"), exist_ok=True)
os.makedirs(os.path.join(RESULT_DIR, "mask"), exist_ok=True)

# --------------------------------
# Dashboard (Upload Page)
# --------------------------------
@app.route("/")
def dashboard():
    return render_template("upload.html")

# --------------------------------
# Upload + Analyze (Single & Batch)
# --------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    view = request.form.get("view", "dots")

    # 🔹 Support batch uploads
    images = request.files.getlist("images")

    # 🔹 Fallback to single-image input
    if not images or images[0].filename == "":
        single_image = request.files.get("image")
        if single_image:
            images = [single_image]

    if not images:
        return "No image uploaded", 400

    results = []

    for image in images:
        if image.filename == "":
            continue

        # -------------------------
        # Save original image
        # -------------------------
        filename, img_path = save_image(image, UPLOAD_DIR)

        # -------------------------
        # Analyze image
        # -------------------------
        result_path, count, confluency = analyze_image(
            image_path=img_path,
            filename=filename,
            mode=view
        )

        # -------------------------
        # Audit logging
        # -------------------------
        log_event(
            action="IMAGE_ANALYSIS_BATCH" if len(images) > 1 else "IMAGE_ANALYSIS",
            image_name=filename,
            model_used="my_cells_v2",
            cell_count=count,
            confluency=confluency,
            view_mode=view,
            ip_address=request.remote_addr
        )

        # -------------------------
        # Collect result
        # -------------------------
        results.append({
            "filename": filename,
            "original_image": f"/uploads/{filename}",
            "result_image": result_path,
            "count": count,
            "confluency": confluency
        })

    if not results:
        return "No valid images processed", 400

    # --------------------------------
    # SINGLE IMAGE → result.html
    # --------------------------------
    if len(results) == 1:
        r = results[0]
        return render_template(
            "result.html",
            original_image=r["original_image"],
            result_image=r["result_image"],
            count=r["count"],
            confluency=r["confluency"]
        )

    # --------------------------------
    # BATCH SUMMARY CALCULATIONS
    # --------------------------------
    total_cells = sum(r["count"] for r in results)
    avg_confluency = round(
        sum(r["confluency"] for r in results) / len(results), 2
    )

    # Density classification
    if avg_confluency < 30:
        density = "Low"
        density_class = "success"
    elif avg_confluency < 70:
        density = "Medium"
        density_class = "warning"
    else:
        density = "High"
        density_class = "danger"

    # --------------------------------
    # BATCH → batch_result.html
    # --------------------------------
    return render_template(
        "batch_result.html",
        results=results,
        total_images=len(results),
        total_cells=total_cells,
        avg_confluency=avg_confluency,
        density=density,
        density_class=density_class
    )

# --------------------------------
# Serve uploaded images
# --------------------------------
@app.route("/uploads/<path:filename>")
def serve_uploads(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# --------------------------------
# Serve result images
# --------------------------------
@app.route("/results/<path:filename>")
def serve_results(filename):
    return send_from_directory(RESULT_DIR, filename)

# --------------------------------
# Audit logs page
# --------------------------------
@app.route("/audit")
def audit():
    logs = mongo.db.audit_logs.find().sort("timestamp", -1)
    return render_template("audit.html", logs=logs)

# --------------------------------
# Run App
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

