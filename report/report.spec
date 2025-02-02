# -*- mode: python ; coding: utf-8 -*-
from os.path import join, basename, dirname, exists
from os import walk, makedirs
from shutil import copyfile

block_cipher = None

# 分析 report.py
a_report = Analysis(
    ['report.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz_report = PYZ(a_report.pure, a_report.zipped_data, cipher=block_cipher)

exe_report = EXE(
    pyz_report,
    a_report.scripts,
    [],
    exclude_binaries=True,
    name='report',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='internal',
)

# 分析 report_gui.py
a_gui = Analysis(
    ['report_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz_gui = PYZ(a_gui.pure, a_gui.zipped_data, cipher=block_cipher)

exe_gui = EXE(
    pyz_gui,
    a_gui.scripts,
    [],
    exclude_binaries=True,
    name='report_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='internal',
)

# 合并两个 COLLECT 对象
coll = COLLECT(
    exe_report,
    exe_gui,
    a_report.binaries + a_gui.binaries,
    a_report.zipfiles + a_gui.zipfiles,
    a_report.datas + a_gui.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='report',  # 使用统一的目录
)

# 复制额外所需的文件
my_files = ['report.py', 'report_gui.py']
my_folders = ['Aut']
dest_root = join('dist', basename(coll.name))
# 遍历 my_folders 中的文件夹，仅添加 .py 文件
for folder in my_folders:
    for dirpath, dirnames, filenames in walk(folder):
        for filename in filenames:
            if filename.endswith('.py'):  # 仅包含 .py 文件
                my_files.append(join(dirpath, filename))
for file in my_files:
    if not exists(file):
        continue
    dest_file = join(dest_root, file)
    dest_folder = dirname(dest_file)
    makedirs(dest_folder, exist_ok=True)
    copyfile(file, dest_file)