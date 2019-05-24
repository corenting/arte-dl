from arte_dl.commands.video.downloader import get_json_from_video_url, get_infos_from_json_url, download_video_from_url
from arte_dl.commands.video.utils import get_safe_filename


def get_language_versions(items):
    ret_versions = []
    for i in items:
        if i['versionLibelle'] not in ret_versions:
            ret_versions.append(i['versionLibelle'])
    return ret_versions


def make_cli_choice(input_tile, input_items):
    # Print the list of choices
    iteration = 1
    for l in input_items:
        print('{0} - {1}'.format(str(iteration), l))
        iteration += 1

    # Ask for selection
    selected_value = None
    while selected_value is None:
        str_value = input('{0} choice: '.format(input_tile))

        try:
            int_value = int(str_value)
            if 0 < int_value < len(input_items):
                selected_value = int_value
            else:
                raise ValueError()
        except ValueError:
            print('Invalid choice, please specify a number between 1 and {0}'.format(len(input_items)))
    return selected_value - 1


def download_video(video_url):
    """
    Process video download
    :param video_url: the URL of the video to download
    """
    # Get JSON
    url = get_json_from_video_url(video_url)
    json = get_infos_from_json_url(url)
    video_title = json['VTI']
    print("Title: " + video_title)

    # Build list of versions
    versions_list = []
    for item_title in json['VSR']:
        item = json['VSR'][item_title]
        versions_list.append(item)

    # Prompt user to select language
    languages_list = get_language_versions(versions_list)
    selected_language = languages_list[make_cli_choice('Language', languages_list)]
    print(selected_language)

    # Get videos with selected language
    resolution_list = []
    for item in versions_list:
        # Ignore other languages / formats
        if item['versionLibelle'] != selected_language or item['mediaType'] != 'mp4':
            continue

        # Insert with checking if the URL is unique (duplicate URLs may happen in the API)
        item_in_list_with_url = next((x for x in resolution_list if x['url'] == item['url']), None)
        if item_in_list_with_url is None:
            resolution_list.append(item)
    resolution_list.sort(key=lambda x: x['width'], reverse=True)  # sort by resolution

    # Prompt user to select resolution
    resolution_display_list = [
        '{0}x{1}'.format(str(v['width']), str(v['height'])) for v in resolution_list
    ]
    selected_video = resolution_list[make_cli_choice('Version', resolution_display_list)]

    download_video_from_url(selected_video['url'], '{0}.mp4'.format(get_safe_filename(video_title)))
