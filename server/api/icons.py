import os

from flask import jsonify, request

from util.config import SECRET_KEY

from . import api_bp

UPLOAD_ICON_FOLDER = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "templates", "exe_icon"))
os.makedirs(UPLOAD_ICON_FOLDER, exist_ok=True)


@api_bp.route("/upload_exeIcon", methods=["POST"])
def upload_exeIcon():
    key = request.headers.get("API-KEY")
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key"}), 403
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No selected files"}), 400
    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        if file and file.filename.lower().endswith(".png"):
            filename = file.filename
            file_path = os.path.join(UPLOAD_ICON_FOLDER, filename)
            file.save(file_path)
            saved_files.append(filename)
        else:
            return jsonify({"error": "Invalid file type only support .png"}), 400
    return jsonify({"message": "File uploaded successfully", "filename": saved_files}), 200


@api_bp.route("/get_allIcon", methods=["GET"])
def get_allIcon():
    try:
        all_entries = os.listdir(UPLOAD_ICON_FOLDER)
        filenames = [entry.split(".png")[0] for entry in all_entries if os.path.isfile(os.path.join(UPLOAD_ICON_FOLDER, entry))]
        return jsonify(filenames), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @api_bp.route("/exe_icon/<path:filename>", methods=["GET"])
# def exe_icon(filename):
#     safe_name = os.path.basename(filename or "")
#     if not safe_name:
#         return jsonify({"error": "Invalid filename"}), 400

#     # Only allow PNG files
#     if not safe_name.lower().endswith(".png"):
#         return jsonify({"error": "Invalid file type, only .png allowed"}), 400

#     file_path = os.path.join(UPLOAD_ICON_FOLDER, safe_name)
#     if not os.path.isfile(file_path):
#         return jsonify({"error": "File not found"}), 404

#     return send_from_directory(UPLOAD_ICON_FOLDER, safe_name)
