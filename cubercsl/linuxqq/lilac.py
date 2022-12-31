import re

from lilaclib import *

def _get_md5_prefix():
    url = 'https://im.qq.com/rainbow/linuxQQDownload'
    r = s.get(url)
    if r.status_code != 200:
        raise Exception('Failed to get download url')
    print(r.text)
    m = re.search(r'https://dldir1\.qq\.com/qqfile/qq/QQNT/([0-9a-f]{8})/linuxqq', r.text)
    if not m:
        raise Exception('Failed to parse download url')
    return m.group(1)


def pre_build():
    md5_prefix = _get_md5_prefix()
    print(f'Found md5 prefix: {md5_prefix}')
    pkgver = _G.newver.lstrip('v').replace('-', '_')
    update_pkgver_and_pkgrel(pkgver)
    url = 'https://im.qq.com/rainbow/linuxQQDownload'
    for line in edit_file('PKGBUILD'):
        if line.startswith('_md5_prefix='):
            line = f'_md5_prefix={md5_prefix}'
        print(line)

def post_build():
    git_pkgbuild_commit()

