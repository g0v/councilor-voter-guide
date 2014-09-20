import os
import subprocess


def append_contact(item, contact_type, label, value):
    item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})


def append_contact_list(item, contact_type, label, value_list):
    for value in value_list:
        item['contact_details'].append({'type': contact_type, 'label': label, 'value': value})


def download(url, file_path, force_redownload=False):
    skipped = not force_redownload and os.path.exists(file_path)
    retcode = None

    if not skipped:
        cmd = 'wget -c -O "%s" %s' % (file_path, url)
        retcode = subprocess.call(cmd, shell=True)

    return {
        'success': skipped or retcode == 0,
        'skipped': skipped,
        'code': retcode
    }
