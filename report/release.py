import os

import requests
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


def create_release(
    api_url,
    platform,
    owner,
    repo,
    access_token,
    tag_name,
    release_name,
    release_description,
):
    url = f"{api_url}/repos/{owner}/{repo}/releases"
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "tag_name": tag_name,
        "name": release_name,
        "body": release_description,
        "target_commitish": "master",
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Release created successfully on {platform}.")
        return response.json()
    elif response.status_code == 400 and "该标签已经存在发行版" in response.text:
        release_url = f"{api_url}/repos/{owner}/{repo}/releases/tags/{tag_name}"
        r = requests.get(release_url, headers=headers)
        if r.status_code == 200:
            print("Existing release found.")
            return r.json()
        else:
            print(f"Failed to get release on {platform}: {r.status_code} {r.text}")
            exit(0)
    else:
        print(f"Failed to create release on {platform}: {response.status_code} {response.text}")
        exit(0)


def upload_asset(api_url, platform, owner, repo, access_token, release_id, file_path):
    if platform == "gitee":
        url = f"{api_url}/repos/{owner}/{repo}/releases/{release_id}/attach_files"
        headers = {
            "Authorization": f"token {access_token}",
        }
        file_name = os.path.basename(file_path)
        params = {"name": file_name}

        with open(file_path, "rb") as file:
            files = {"file": (file_name, file)}
            response = requests.post(url, headers=headers, params=params, files=files)
            if response.status_code == 201:
                print(f"Asset '{file_name}' uploaded successfully on {platform}.")
            else:
                print(f"Failed to upload asset on {platform}: {response.status_code} {response.text}")
                exit(0)
    elif platform.lower() == "github":
        url = f"{api_url}/repos/{owner}/{repo}/releases/{release_id}"
        response = requests.get(url, headers={"Authorization": f"token {access_token}"})
        if response.status_code == 200:
            upload_url = response.json()["upload_url"]
            upload_url = upload_url.replace("{?name,label}", "")  # 清理模板参数
            file_name = os.path.basename(file_path)
            headers = {
                "Authorization": f"token {access_token}",
                "Content-Type": "application/octet-stream",
            }
            params = {"name": file_name}
            with open(file_path, "rb") as file:
                response = requests.post(upload_url, headers=headers, params=params, data=file)
                if response.status_code == 201:
                    print(f"Asset '{file_name}' uploaded successfully on {platform}.")
                else:
                    print(f"Failed to upload asset on {platform}: {response.status_code} {response.text}")
                    exit(0)
        else:
            print(f"Failed to get release details on {platform}: {response.status_code} {response.text}")
            exit(0)
    else:
        print("Unsupported platform for upload.")
        exit(0)


def main(
    platform,
    access_token,
    tag_name,
    release_name,
    release_description,
    files: list[str],
):
    repo = "seeme"
    if platform.lower() == "github":
        api_url = "https://api.github.com"
        owner = "2412322029"
    elif platform.lower() == "gitee":
        api_url = "https://gitee.com/api/v5"
        owner = "qwe2412322029"
    else:
        raise ValueError("Unsupported platform. Use 'github' or 'gitee'.")

    print(f"Creating release on {platform}...")
    release = create_release(
        api_url,
        platform,
        owner,
        repo,
        access_token,
        tag_name,
        release_name,
        release_description,
    )

    if release:
        release_id = release["id"]
        for f in files:
            print(f"Uploading asset '{f}'...")
            upload_asset(api_url, platform, owner, repo, access_token, release_id, f)


if __name__ == "__main__":
    c = int(input("(1) gitee,(2) github."))
    if c == 1:
        PLATFORM = "gitee"
        ACCESS_TOKEN = os.environ.get("GITEE_TOKEN")
        if not ACCESS_TOKEN:
            print("env:gitee_token not found")
            exit(0)
    elif c == 2:
        PLATFORM = "github"
        ACCESS_TOKEN = os.environ.get("GITHUB_TOKEN")  # 从环境变量获取GitHub Token
        if not ACCESS_TOKEN:
            print("env:github_token not found")
            exit(0)
    else:
        exit(0)

    from Aut.logger import __version__
    from build import CONFIG

    TAG_NAME = f"v{__version__}"
    RELEASE_NAME = f"v{__version__}"
    files = [
        os.path.join(CONFIG["output_dir"], f"{CONFIG['gui_dir']}.{__version__}.zip"),
        os.path.join(CONFIG["output_dir"], f"{CONFIG['gui_dir']}.{__version__}.zip.sha256.txt"),
    ]

    # 检查文件是否存在
    for f in files:
        if not os.path.exists(f):
            print(f"{f} not found")
            exit(0)

    RELEASE_DESCRIPTION = input("Release description:")
    clog = f"\n\nV{__version__}\n  {RELEASE_DESCRIPTION}"
    print(f"Platform: {PLATFORM}")
    print(f"Tag: {TAG_NAME}")
    print(f"Release name: {RELEASE_NAME}")
    print(f"Files to upload: {files}")
    print(f"Release description: {RELEASE_DESCRIPTION}")
    input("Press Enter to confirm and continue...")

    main(PLATFORM, ACCESS_TOKEN, TAG_NAME, RELEASE_NAME, RELEASE_DESCRIPTION, files)

    # 更新changelog
    with open("changelog.txt", "a", encoding="utf-8") as f:
        f.write(clog)
        print("Changelog updated")
