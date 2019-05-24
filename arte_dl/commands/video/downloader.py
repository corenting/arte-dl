import json
import sys
import urllib

import requests

from arte_dl.commands.video.utils import get_human_readable_file_size


def exit_download_error(url_used):
    print("Error: download error (" + url_used + ")", file=sys.stderr)
    exit(1)


def get_json_from_video_url(video_page):
    try:
        req = requests.get(video_page)
        if req.status_code != 200:
            exit_download_error(video_page)
        page_content = req.content.decode("utf-8")
        req.close()
    except:  # noqa: E722
        return exit_download_error(video_page)

    # Find JSON URL
    try:
        start = 'https://www.arte.tv/player/v3/index.php?json_url='
        end = '&'
        result = (page_content.split(start))[1].split(end)[0]
        return urllib.parse.unquote(result)
    except:  # noqa: E722
        print("Error: cannot extract video metadatas URL from webpage",
              file=sys.stderr)
        exit(1)


def get_infos_from_json_url(json_url):
    try:
        req = requests.get(json_url)
        if req.status_code != 200:
            exit_download_error(json_url)
        json_content = json.loads(req.content.decode("utf-8"))
        req.close()
        return json_content['videoJsonPlayer']
    except:  # noqa: E722
        exit_download_error(json_url)


def download_video_from_url(video_url, filename):
    print('Downloading video...')
    try:
        req = requests.get(video_url, stream=True)
        if req.status_code != 200:
            exit_download_error(video_url)
        total_length = int(req.headers.get('content-length'))
        print('Size: ' + get_human_readable_file_size(total_length))
        downloaded_length = 0
        with open(filename, 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_length += len(chunk)
                    print('Progress: ' +
                          str(int((downloaded_length / total_length) * 100)) +
                          '%', end='\r')

        req.close()
    except:  # noqa: E722
        exit_download_error(video_url)
