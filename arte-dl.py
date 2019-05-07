#!/usr/bin/env python3

import json
import sys
import urllib.parse

import requests


def download_error(url_used):
    print("Error: download error (" + url_used + ")", file=sys.stderr)
    exit(1)


def get_json_url(video_page):
    try:
        req = requests.get(video_page)
        if req.status_code != 200:
            download_error(video_page)
        page_content = req.content.decode("utf-8")
        req.close()
    except:  # noqa: E722
        download_error(video_page)

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


def get_json_infos(json_url):
    try:
        req = requests.get(json_url)
        if req.status_code != 200:
            download_error(json_url)
        json_content = json.loads(req.content.decode("utf-8"))
        req.close()
        return json_content['videoJsonPlayer']
    except:  # noqa: E722
        download_error(json_url)


def get_language_versions(items):
    ret_versions = []
    for i in items:
        if i['versionLibelle'] not in ret_versions:
            ret_versions.append(i['versionLibelle'])
    return ret_versions


def select_number(max_choice, input_type):
    selected_value = None
    while selected_value is None:
        str_value = input(input_type + ' choice: ')
        try:
            int_value = int(str_value)
            if 0 < int_value < max_choice:
                selected_value = int_value
        except:  # noqa: E722
            continue
    return selected_value


def download_video(video_url, filename):
    print('Downloading video...')
    try:
        req = requests.get(video_url, stream=True)
        if req.status_code != 200:
            download_error(video_url)
        total_length = int(req.headers.get('content-length'))
        print('Size: ' + sizeof_fmt(total_length))
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
        download_error(video_url)


def get_safe_filename(title):
    keep_chars = (' ', '.', '_')
    return "".join(c for c in title if c.isalnum() or c in keep_chars).rstrip()


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def main():
    if len(sys.argv) < 2:
        print("Error: no URL provided", file=sys.stderr)
        exit(1)
    # Get JSON
    url = get_json_url(sys.argv[1])
    json = get_json_infos(url)
    print("Title: " + json['VTI'])

    # Build list of versions
    items_list = []
    for item_title in json['VSR']:
        item = json['VSR'][item_title]
        items_list.append(item)

    # Language selection
    languages = get_language_versions(items_list)
    iteration = 1
    for l in languages:
        print(str(iteration) + ' - ' + l)
        iteration += 1
    selected_language = languages[select_number(iteration, 'Language') - 1]
    print(selected_language)

    # Build final items list for selection
    # (deduplicate due to same URL sent multiple times for some files)
    items_with_duplicates = [i for i in items_list if
                             i['versionLibelle'] == selected_language and
                             i['mediaType'] == 'mp4']
    items_with_language = []
    for i in items_with_duplicates:
        already_exist = next(
            (x for x in items_with_language if x['url'] == i['url']),
            None)
        if already_exist is None:
            items_with_language.append(i)
    items_with_language.sort(key=lambda x: x['width'],
                             reverse=True)  # sort by resolution

    # Select version
    video_iter = 1
    for v in items_with_language:
        print(str(video_iter) + ' - ' +
              str(v['width']) +
              'x' + str(v['height']))
        video_iter += 1
    selected_video = items_with_language[select_number(video_iter,
                                                       'Version') - 1]

    download_video(selected_video['url'],
                   get_safe_filename(json['VTI']) + '.mp4')


if __name__ == "__main__":
    main()
