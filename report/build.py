import hashlib
import os
import re
import shutil
import sys
from typing import Tuple

CONFIG = {
    "output_dir": "dist",
    "gui_dir": "report_gui.dist",
    "cli_dir": "report.dist",
    "gui_filename": "report.exe",
    "cli_filename": "report_cli.exe",
    "icon_source": "icon.ico",
    "update_source": "update.exe",
    "upx_path": "upx",
    "7z_path": "7z",
    "version_file": "Aut/logger.py"
}


class BuildConfig:
    def __init__(self):
        self.current_version = None
        self.new_version = None
        self.build_gui = False
        self.build_cli = False
        self.use_upx = False
        self.use_7z = False


def print_color(text: str, color_code: str) -> None:
    print(f"\033[{color_code}m{text}\033[0m", flush=True)


def print_header(text: str) -> None:
    print_color(f"\n{'-' * 30}\n{text}\n{'-' * 30}", "94")


def check_tool(tool_name: str) -> None:
    r = shutil.which(tool_name)
    if r:
        print_color(f"use {tool_name} -> {r}", "92")
    else:
        print_color(f"错误：未找到必要工具 {tool_name}，请安装并添加到PATH环境变量", "91")
        exit(1)


def execute_command(command: str) -> None:
    print_color(f"执行命令: {command}", "92")
    try:
        return_code = os.system(command)
        if return_code != 0:
            print_color(f"命令执行失败: {command}\n退出代码: {return_code}", "91")
            sys.exit(return_code)
    except Exception as e:
        print_color(f"命令执行失败: {command}\n错误信息: {str(e)}", "91")
        sys.exit(1)


def get_version_info() -> Tuple[bool, str]:
    version_file = CONFIG["version_file"]
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print_color(f"错误：版本文件 {version_file} 不存在", "91")
        exit(1)

    match = re.search(r'__version__\s*=\s*"(\d+\.\d+\.\d+)"', content)
    if not match:
        print_color("错误：版本信息格式不正确", "91")
        exit(1)

    current_version = match.group(1)
    print_header(f"当前版本: {current_version}")

    # 版本递增逻辑
    parts = list(map(int, current_version.split(".")))
    choices = [
        (f"补丁版本 ({current_version} → {parts[0]}.{parts[1]}.{parts[2] + 1})", 2),
        (f"次版本号 ({current_version} → {parts[0]}.{parts[1] + 1}.0)", 1),
        (f"主版本号 ({current_version} → {parts[0] + 1}.0.0)", 0),
        ("不更新版本", None)
    ]

    for i, (desc, _) in enumerate(choices, 1):
        print_color(f"{i}. {desc}", "93")

    while True:
        choice = input("请选择版本更新方式 (1-4): ").strip()
        if choice == "4":
            return False, current_version
        if choice in ("1", "2", "3"):
            level = choices[int(choice) - 1][1]
            if level is None:
                return False, current_version
            break
        print_color("无效输入，请重新选择", "91")

    # 更新版本号
    if level == 0:  # 主版本号递增
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif level == 1:  # 次版本号递增
        parts[1] += 1
        parts[2] = 0
    elif level == 2:  # 补丁版本递增
        parts[2] += 1
    new_version = ".".join(map(str, parts))
    input(f"{new_version=}(Press Enter to continue)")
    try:
        with open(version_file, "w", encoding="utf-8") as f:
            new_content = re.sub(
                r'__version__\s*=\s*".*?"',
                f'__version__ = "{new_version}"',
                content
            )
            f.write(new_content)
    except IOError as e:
        print_color(f"写入版本文件失败: {str(e)}", "91")
        exit(1)

    return True, new_version


def build_gui_app(config: BuildConfig) -> None:
    print_header("开始构建GUI应用程序")
    command = (
        f"nuitka --standalone --follow-imports --lto=yes "
        f"--enable-plugin=tk-inter --windows-icon-from-ico={CONFIG['icon_source']} "
        f"--output-filename={CONFIG['gui_filename']} --output-dir={CONFIG['output_dir']} "
        f"--no-deployment-flag=self-execution --windows-console-mode=disable "
        f"--product-name=report --file-version={config.new_version}.0 report_gui.py"
    )
    execute_command(command)

    # 处理图标文件
    icon_src = CONFIG["icon_source"]
    dest_dir = os.path.join(CONFIG["output_dir"], CONFIG["gui_dir"])
    icon_dest = os.path.join(dest_dir, "icon.ico")

    try:
        if os.path.exists(icon_src):
            shutil.copy(icon_src, icon_dest)
            print_color("图标文件已复制到目标目录", "92")
        else:
            print_color("警告：未找到图标文件，跳过复制", "93")
    except IOError as e:
        print_color(f"复制图标文件失败: {str(e)}", "91")
    try:
        if os.path.exists(CONFIG["update_source"]):
            shutil.copy(CONFIG["update_source"], os.path.join(dest_dir, "update.exe"))
            print_color("update.exe文件已复制到目标目录", "92")
        else:
            print_color("警告：未找到update.exe，跳过复制", "93")
    except IOError as e:
        print_color(f"复制update.exe文件失败: {str(e)}", "91")


def build_cli_app(config: BuildConfig) -> None:
    print_header("开始构建CLI应用程序")
    command = (
        f"nuitka --standalone --follow-imports --lto=yes "
        f"--product-name=report_cli --file-version={config.new_version}.0 "
        f"--output-filename={CONFIG['cli_filename']} --output-dir={CONFIG['output_dir']} report.py"
    )
    execute_command(command)


def process_upx() -> None:
    """使用UPX压缩可执行文件"""
    print_header("使用UPX压缩")
    source_path = os.path.join(
        CONFIG["output_dir"],
        CONFIG["cli_dir"],
        CONFIG["cli_filename"]
    )
    dest_dir = os.path.join(CONFIG["output_dir"], CONFIG["gui_dir"])

    try:
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, CONFIG["cli_filename"])
        shutil.copy(source_path, dest_path)
        print_color("已复制CLI可执行文件到GUI目录", "92")
    except IOError as e:
        print_color(f"文件操作失败: {str(e)}", "91")
        exit(1)

    upx_cmd = f"{CONFIG['upx_path']} {dest_path}"
    execute_command(upx_cmd)


def calculate_sha256(file_path: str) -> str:
    """计算文件的SHA256哈希值"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()


def create_7z_archive(config: BuildConfig) -> None:
    print_header("创建7z压缩包")
    source_dir = os.path.join(CONFIG["output_dir"], CONFIG["gui_dir"])
    if not os.path.exists(source_dir):
        print_color(f"错误：目录不存在 {source_dir}", "91")
        return

    archive_name = f"{CONFIG['gui_dir']}.{config.new_version}.zip"
    archive_path = os.path.join(CONFIG["output_dir"], archive_name)

    command = (
        f"cd {CONFIG["output_dir"]} && {CONFIG['7z_path']} a -tzip {archive_name} {CONFIG["gui_dir"]}\\*"
    )
    execute_command(command)
    print_color(f"已创建压缩包: {archive_path}", "92")
    sha256_hash = calculate_sha256(archive_path)
    print_color(f"压缩包的SHA256哈希值: {sha256_hash}", "92")
    hash_file_path = archive_path + ".sha256.txt"
    with open(hash_file_path, "w") as f:
        f.write(sha256_hash)
    print_color(f"哈希值已写入文件: {hash_file_path}", "92")


def main():
    config = BuildConfig()

    # 版本处理
    version_updated, new_version = get_version_info()
    if not version_updated:
        print_color("版本未更新", "93")
        # return
    config.new_version = new_version

    config.build_gui = input("是否构建GUI应用？ (y/n): ").lower() == "y"
    config.build_cli = input("是否构建CLI应用？ (y/n): ").lower() == "y"
    config.use_upx = input("是否使用UPX压缩CLI？ (y/n): ").lower() == "y"
    config.use_7z = input("是否创建7z压缩包？ (y/n): ").lower() == "y"

    # 前置检查
    if config.use_upx:
        check_tool(CONFIG["upx_path"])
    if config.use_7z:
        check_tool(CONFIG["7z_path"])
    if config.build_gui or config.build_cli:
        check_tool("nuitka")

    # 执行构建流程
    try:
        if config.build_gui:
            build_gui_app(config)
        if config.build_cli:
            build_cli_app(config)
        if config.use_upx:
            process_upx()
        if config.use_7z:
            create_7z_archive(config)
    except KeyboardInterrupt:
        print_color("\n用户中断构建流程", "91")
        exit(1)

    print_header("构建流程完成")


if __name__ == "__main__":
    main()
