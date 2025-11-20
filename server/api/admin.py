import os
import re
import time

from flask import Response, jsonify, request

from util.config import SECRET_KEY
from util.rediscache import r

from . import api_bp

logpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log")
if not os.path.exists(logpath):
    os.makedirs(logpath)
MAX_READ_BYTES = 2 * 1024 * 1024  # 最大读取 2MB
ALLOWED_EXT = (".log", ".txt", ".json")


@api_bp.route("/redis", methods=["GET"])
def redis_info():
    if request.headers.get("API-KEY") != SECRET_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    try:
        info = r.info()
        return jsonify(info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/logfilelist", methods=["GET"])
def logfilelist():
    if request.headers.get("API-KEY") != SECRET_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    try:
        files = []
        for entry in os.listdir(logpath):
            full_path = os.path.join(logpath, entry)
            if os.path.isfile(full_path) and (entry.lower().endswith(ALLOWED_EXT) or entry.lower().split(".")[:-1].endswith(".log")):
                try:
                    size = os.path.getsize(full_path)
                    mtime = os.path.getmtime(full_path)
                    mtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
                except Exception:
                    size = None
                    mtime_str = None
                files.append({"name": entry, "size": size, "mtime": mtime_str})
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/logfile", methods=["GET"])
def logfile():
    if request.headers.get("API-KEY") != SECRET_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    filename = request.args.get("filename", "").strip()
    if not filename:
        return jsonify({"error": "Filename parameter is required"}), 400
    basename = os.path.basename(filename)
    if basename != filename:
        return jsonify({"error": "Invalid filename"}), 400
    if not re.match(r"^[A-Za-z0-9_.-]+$", basename):
        return jsonify({"error": "Filename contains invalid characters"}), 400
    if not basename.lower().endswith(ALLOWED_EXT):
        return jsonify({"error": "Unsupported file extension"}), 400
    log_file = os.path.join(logpath, basename)
    try:
        if os.path.commonpath([os.path.abspath(log_file), os.path.abspath(logpath)]) != os.path.abspath(logpath):
            return jsonify({"error": "Invalid filename path"}), 400
    except Exception:
        return jsonify({"error": "Invalid filename path"}), 400
    if not os.path.exists(log_file) or not os.path.isfile(log_file):
        return jsonify({"error": "File not found"}), 404

    # 行分页参数：lines（每页行数，默认1000），page（从1开始），或直接使用 start_line（从0开始）
    lines_arg = request.args.get("lines")
    page_arg = request.args.get("page")
    start_line_arg = request.args.get("start_line")

    MAX_LINES_PER_PAGE = 5000
    DEFAULT_LINES = 1000

    def read_lines_range(path, start, count, max_probe_extra=1):
        """
        从 start(0-based) 开始读取 count 行，返回 (joined_text, returned_lines, end_index, has_more)
        为判断是否还有更多行，会尝试读取 count + max_probe_extra 行。
        """
        returned = []
        returned_count = 0
        end_index = start - 1
        has_more = False
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for idx, line in enumerate(f):
                if idx < start:
                    continue
                if returned_count < count:
                    returned.append(line.rstrip("\n"))
                    returned_count += 1
                    end_index = idx
                else:
                    # 读取到额外一行，说明还有更多
                    has_more = True
                    break
        return ("\n".join(returned), returned_count, end_index, has_more)

    try:
        size = os.path.getsize(log_file)

        # 如果传递了分页/行参数，按行处理
        if lines_arg is not None or page_arg is not None or start_line_arg is not None:
            try:
                lines = int(lines_arg) if lines_arg is not None else DEFAULT_LINES
                if lines <= 0:
                    return jsonify({"error": "lines must be > 0"}), 400
                if lines > MAX_LINES_PER_PAGE:
                    lines = MAX_LINES_PER_PAGE
            except ValueError:
                return jsonify({"error": "invalid lines parameter"}), 400

            if start_line_arg is not None:
                try:
                    start_line = int(start_line_arg)
                    if start_line < 0:
                        raise ValueError()
                except ValueError:
                    return jsonify({"error": "invalid start_line parameter"}), 400
            else:
                # 使用 page 参数（默认第1页）
                try:
                    page = int(page_arg) if page_arg is not None else 1
                    if page < 1:
                        raise ValueError()
                except ValueError:
                    return jsonify({"error": "invalid page parameter"}), 400
                start_line = (page - 1) * lines

            content, returned_lines, end_idx, has_more = read_lines_range(log_file, start_line, lines)
            headers = {
                "X-File-Size": str(size),
                "X-Start-Line": str(start_line),
                "X-Returned-Lines": str(returned_lines),
                "X-End-Line": str(end_idx if returned_lines > 0 else max(start_line - 1, 0)),
                "X-Has-More": "true" if has_more else "false",
            }
            return Response(content, mimetype="text/plain", headers=headers), 200

        # 原始按字节行为：文件较小返回全部，大文件返回尾部 MAX_READ_BYTES
        if size <= MAX_READ_BYTES:
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            headers = {"X-File-Size": str(size), "X-Returned-Bytes": str(len(content.encode("utf-8"))), "X-Partial": "false"}
            return Response(content, mimetype="text/plain", headers=headers), 200
        else:
            with open(log_file, "rb") as f:
                f.seek(-MAX_READ_BYTES, os.SEEK_END)
                tail = f.read()
            text = tail.decode("utf-8", errors="replace")
            header = f"--- FILE TRUNCATED: returned last {MAX_READ_BYTES} bytes of {basename} ---\n"
            headers = {"X-File-Size": str(size), "X-Returned-Bytes": str(len(tail)), "X-Partial": "true", "X-Range-Start": str(max(0, size - MAX_READ_BYTES)), "X-Range-End": str(size - 1)}
            return Response(header + text, mimetype="text/plain", headers=headers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/auth", methods=["GET"])
def auth():
    if request.headers.get("API-KEY") != SECRET_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    else:
        return jsonify({"status": "success"}), 200
