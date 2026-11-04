import base64
import os
import binascii
import json
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, parse_qs

import requests

requests.packages.urllib3.disable_warnings()

channels = {
    "stable": "msedge-stable-win",
}

check_version_url = (
    "https://msedge.api.cdp.microsoft.com/api/v2/contents/Browser/namespaces/Default/names/{"
    "0}/versions/latest?action=select"
)
get_download_link_url = (
    "https://msedge.api.cdp.microsoft.com/api/v1.1/internal/contents/Browser/namespaces/Default"
    "/names/{0}/versions/{1}/files?action=GenerateDownloadInfo"
)

results = {}


def check_version(appid):
    # 必须包含 UA 头，否则报错
    headers = {"User-Agent": "Microsoft Edge Update/1.3.183.29;winhttp"}
    data = {
        "targetingAttributes": {
            "IsInternalUser": True,
            "Updater": "MicrosoftEdgeUpdate",
            "UpdaterVersion": "1.3.183.29",
        }
    }
    response = requests.post(
        check_version_url.format(appid), json=data, headers=headers, verify=False
    )

    if response.status_code == 200:
        content_id = response.json().get("ContentId")
        if content_id:
            version = content_id.get("Version")
            return version
        else:
            print("ContentId not found in the response.")
    else:
        print(
            "Error: Unable to fetch version information. Status code:",
            response.status_code,
        )

    return None


def get_download_link(appid, version):
    headers = {"User-Agent": "Microsoft Edge Update/1.3.183.29;winhttp"}
    response = requests.post(
        get_download_link_url.format(appid, version), headers=headers, verify=False
    )

    if response.status_code == 200:
        download_info = response.json()
        if download_info:
            # 首先按照字节大小从大到小排序
            download_info.sort(key=lambda x: x.get("SizeInBytes", 0), reverse=True)
            item = download_info[0]
            file_id = item.get("FileId", "")
            url = item.get("Url", "")
            size_in_bytes = item.get("SizeInBytes", 0)
            hashes = item.get("Hashes", {})
            sha1 = hashes.get("Sha1", "")
            sha256 = hashes.get("Sha256", "")

            return {
                "file_name": file_id,
                "url": url,
                "size_in_bytes": size_in_bytes,
                "Sha1": sha1,
                "Sha256": sha256,
            }
        else:
            print("Download information not found in the response.")
    else:
        print(
            "Error: Unable to fetch download information. Status code:",
            response.status_code,
        )

    return None


def get_info(appid):
    version = check_version(appid)
    if version:
        name = appid
        info = get_download_link(appid, version)
        if info:
            info["version"] = version
            return name, info
        else:
            print("Error: Unable to obtain download information for", appid)
    else:
        print("Error: Unable to obtain version information for", appid)
    return None


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


def load_json():
    global results
    if not os.path.exists("data.json"):
        results = {}
        return
    try:
        with open("data.json", "r") as f:
            results = json.load(f)
            if not results:
                results = {}
    except (json.JSONDecodeError, ValueError):
        results = {}


# Microsoft direct links last ~9-10 days; the expiry is in the URL P1 param.
# When the version is unchanged, refresh only within REFRESH_BEFORE_EXPIRY of
# expiry, so links are not rewritten every hour (churn).
REFRESH_BEFORE_EXPIRY = timedelta(days=3)


def link_expiry(url):
    p1 = parse_qs(urlparse(url).query).get("P1", [None])[0]
    return int(p1) if p1 and p1.isdigit() else 0


def fetch():
    now_ts = datetime.now(timezone.utc).timestamp()
    for channel, appid in channels.items():
        for arch in ["x64"]:
            info_result = get_info(f"{appid}-{arch}")
            if info_result is not None:
                name, info = info_result
            else:
                print("Error: Unable to get info for", f"{appid}-{arch}")
                continue
            if name not in results:
                results[name] = info
            elif version_tuple(info["version"]) > version_tuple(
                results[name]["version"]
            ):
                results[name] = info
            elif (
                link_expiry(results[name].get("url", "")) - now_ts
                < REFRESH_BEFORE_EXPIRY.total_seconds()
            ):
                results[name] = info
            else:
                print("ignore", name, info["version"])


suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def replace_http_to_https():
    for name, info in results.items():
        results[name]["url"] = (
            results[name]
            .get("url", "")
            .replace("http://msedge.b", "https://msedge.sb")
        )


def decode_sha256_base64():
    for name, info in results.items():
        sha256_base64 = info.get("Sha256", "")
        if (
            sha256_base64 and len(sha256_base64) != 64
        ):  # Only decode if not already decoded
            try:
                sha256_decoded = base64.b64decode(sha256_base64).hex()
                results[name]["Sha256"] = sha256_decoded
            except binascii.Error:
                print(f"Error: Unable to decode base64 for {name}")

def anchor(title):
    s = "".join(c for c in title.lower() if c.isalnum() or c in " -")
    return s.replace(" ", "-")

def save_json():
    with open("data.json", "w") as f:
        json.dump(results, f, indent=4)


def main():
    load_json()
    fetch()
    replace_http_to_https()
    decode_sha256_base64()
    save_json()


if __name__ == "__main__":
    main()