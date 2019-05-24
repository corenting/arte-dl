def get_safe_filename(title):
    """
    Get a safe string to use as a filename
    :param title: your target file title
    :return: the filename to use
    :rtype: str
    """
    keep_chars = (' ', '.', '_')
    return "".join(c for c in title if c.isalnum() or c in keep_chars).rstrip()


def get_human_readable_file_size(num, suffix='B'):
    """
    Convert a number of bytes to a human readable string
    :param num: the number of bytes
    :param suffix: the suffix you want to use for the units
    :return: the size in a huma-readable string
    :rtype: str
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
