from lilaclib import *

def pre_build():
    pkgver = _G.newver.lstrip('v').replace('-', '_')
    update_pkgver_and_pkgrel(pkgver)

def post_build():
    git_pkgbuild_commit()

