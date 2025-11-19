import hashlib
import os
import sys

from dotenv import load_dotenv
from fabric import Connection

# 排除文件和文件夹
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    "venv",
    ".venv",
    "exe_icon",
    "log",
    "logs",
    ".ruff_cache",
}
EXCLUDE_FILES = {
    ".pre-commit-config.yaml",
    ".env",
    "config-example.toml",
    "data.json",
    "sum.txt",
    "deploy.py",
    "Caddyfile",
}
sum_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sum.txt")
# remote_sum_url = "http://127.0.0.1:5000/get_filesum"
remote_sum_url = "https://i.not404.cc/get_filesum"
# 加载.env文件中的配置
load_dotenv()
REMOTE_HOST = os.getenv("REMOTE_HOST")  # 远程服务器IP或域名
REMOTE_USER = os.getenv("REMOTE_USER")  # 远程服务器用户名
REMOTE_PORT = int(os.getenv("REMOTE_PORT", 22))  # SSH端口，默认为22
REMOTE_DIR = os.getenv("REMOTE_DIR")  # 远程服务器目标目录
PYPATH = os.getenv("PYPATH")  # 远程服务器Python路径


def get_sum_by_ssh():
    # 验证必要配置
    if not REMOTE_HOST or not REMOTE_USER or not REMOTE_DIR or not PYPATH:
        print("SSH 配置不完整：请确保 REMOTE_HOST、REMOTE_USER、REMOTE_DIR 和 PYPATH 已设置。")
        return None
    try:
        with Connection(host=REMOTE_HOST, user=REMOTE_USER, port=REMOTE_PORT) as conn:
            # 在远程生成 sum.txt
            gen_cmd = f"{PYPATH} {REMOTE_DIR}/sum.py generate"
            try:
                gen_result = conn.run(gen_cmd, hide=True, warn=True)
            except Exception as e:
                print(f"执行远程生成命令时出错：{e}")
                return None

            if not gen_result.ok:
                # 打印远程命令的输出以便排查，但仍尝试读取文件
                stderr_or_out = gen_result.stderr or gen_result.stdout
                print(f"远程生成命令返回非零状态：{gen_result.exited}\n{stderr_or_out}")

            # 读取远程 sum.txt
            cat_cmd = f"cat {REMOTE_DIR}/sum.txt"
            try:
                cat_result = conn.run(cat_cmd, hide=True, warn=True)
            except Exception as e:
                print(f"读取远程 sum.txt 时出错：{e}")
                return None

            if cat_result.ok:
                return cat_result.stdout
            else:
                stderr_or_out = cat_result.stderr or cat_result.stdout
                print(f"读取远程 sum.txt 返回非零状态：{cat_result.exited}\n{stderr_or_out}")
                return None
    except Exception as e:
        print(f"建立 SSH 连接时发生错误：{e}")
        return None


# 计算文件哈希
def calculate_file_hash(file_path, hash_algorithm="sha256"):
    """
    计算文件的哈希值
    :param file_path: 文件路径
    :param hash_algorithm: 哈希算法，默认使用 sha256
    :return: 文件的哈希值
    """
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def calculate_directory_hash(directory_path, hash_algorithm="sha256"):
    """
    计算目录中所有文件的哈希值
    :param directory_path: 目录路径
    :param hash_algorithm: 哈希算法，默认使用 sha256
    :return: 目录中所有文件的哈希值字典
    """
    dir_hashes = {}
    for root, dirs, files in os.walk(directory_path):
        # 排除指定的文件夹
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file in EXCLUDE_FILES:
                continue
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory_path)
            dir_hashes[relative_path] = calculate_file_hash(file_path, hash_algorithm)
    return dir_hashes


def generate_sum_txt():
    directory_path = os.path.dirname(os.path.abspath(__file__))
    dir_hashes = calculate_directory_hash(directory_path)
    with open(sum_file_path, "w", encoding="utf-8") as f:
        for relative_path, file_hash in dir_hashes.items():
            f.write(f"{relative_path}: {file_hash}\n")
    print(f"sum.txt generated, path: {sum_file_path}")


# 对比本地和远程的sum.txt, 找出远程没有本地有的文件或者本地sum不同的文件
def compare_sum_txt():
    def normalize_path(p):
        # 统一为 posix 风格，去掉前导 ./ 或 /
        p = p.replace("\\", "/")
        if p.startswith("./"):
            p = p[2:]
        return p.lstrip("/")

    generate_sum_txt()
    with open(sum_file_path, "r", encoding="utf-8") as f:
        local_lines = [line.strip() for line in f if line.strip()]

    def parse_lines(lines):
        d = {}
        for line in lines:
            if ":" in line:
                path, h = line.split(":", 1)
                path = normalize_path(path.strip())
                d[path] = h.strip()
        return d

    local_dict = parse_lines(local_lines)
    remote_text = get_sum_by_ssh()
    remote_dict = parse_lines(remote_text.splitlines())
    only_local = sorted([p for p in local_dict if p not in remote_dict])
    only_remote = sorted([p for p in remote_dict if p not in local_dict])
    different = sorted([p for p in local_dict if p in remote_dict and local_dict[p] != remote_dict[p]])

    if not (only_local or only_remote or different):
        print("本地和远程的 sum.txt 文件一致。")
        return ()

    if only_local:
        print("远程缺失以下本地文件：")
        for p in only_local:
            print(f"  {p}")
    # if only_remote:
    #     print("本地缺失以下远程文件：")
    #     for p in only_remote:
    #         print(f"  {p}")
    if different:
        print("以下文件哈希不同：")
        for p in different:
            print(f"  {p}\n    本地:  {local_dict[p]}\n    远程:  {remote_dict[p]}")

    return only_local, only_remote, different


if __name__ == "__main__":
    if sys.argv[1:2] == ["generate"]:
        generate_sum_txt()
    elif sys.argv[1:2] == ["compare"]:
        compare_sum_txt()
    elif sys.argv[1:2] == ["sum_ssh"]:
        get_sum_by_ssh()
