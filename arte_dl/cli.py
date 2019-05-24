import argparse

from arte_dl.commands.video.main import download_video


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description='CLI video downloader for arte.tv.')
    parser.add_argument('video_url', type=str,
                        help='the URL of the video on arte.tv website')

    args = parser.parse_args()
    download_video(args.video_url)
