from lilaclib import *

def apply_patch(filename, patch):
    patch_proc = subprocess.Popen(["patch", "-p1", filename], stdin=subprocess.PIPE, text=True)
    patch_proc.communicate(patch)

def pre_build():
    aur_pre_build(maintainers=['jonathon'])
    # Apply patches
    apply_patch('PKGBUILD', PATCH)


def post_build():
    aur_post_build()

PATCH=r'''
diff --git a/PKGBUILD b/PKGBUILD
index 1b6d392..f0bfc6b 100644
--- a/PKGBUILD
+++ b/PKGBUILD
@@ -15,10 +15,12 @@ _pkg="NVIDIA-Linux-x86_64-${pkgver}"
 source=('nvidia-drm-outputclass.conf'
         'nvidia-470xx-utils.sysusers'
         'nvidia-470xx.rules'
+        'https://gitlab.com/herecura/packages/nvidia-470xx-dkms/-/raw/9c88952c1504e32ba3656cb0e2afd9286d2a763d/kernel-6.0.patch'
         "https://us.download.nvidia.com/XFree86/Linux-x86_64/${pkgver}/${_pkg}.run")
 sha512sums=('de7116c09f282a27920a1382df84aa86f559e537664bb30689605177ce37dc5067748acf9afd66a3269a6e323461356592fdfc624c86523bf105ff8fe47d3770'
             '4b3ad73f5076ba90fe0b3a2e712ac9cde76f469cd8070280f960c3ce7dc502d1927f525ae18d008075c8f08ea432f7be0a6c3a7a6b49c361126dcf42f97ec499'
             'a0ceb0a6c240cf97b21a2e46c5c212250d3ee24fecef16aca3dffb04b8350c445b9f4398274abccdb745dd0ba5132a17942c9508ce165d4f97f41ece02b0b989'
+            'fac1ed6d07e0ad5cb4591321653cd570729552ff13e4b15a45a556c29edc2904367c463648743ef45788a718cc7aba95446308a99fa17ba97da44467df031915'
             '07aca8ea6aac5592060b4177ef43e9a3a5b2e3bc1a2d5959bf2ae349763fc62ed80b987af5607bf2d9a48e25c4e38e64970bca0177d63bd57a703d47debf5e18')
 
 
@@ -34,6 +36,9 @@ create_links() {
 
 prepare() {
     sh "${_pkg}.run" --extract-only
+    cd "${_pkg}"/kernel
+    patch --verbose --backup --strip=1 --input="${srcdir}"/kernel-6.0.patch
+    cd "${srcdir}"
     cd "${_pkg}"
     bsdtar -xf nvidia-persistenced-init.tar.bz2
 
'''
if __name__ == '__main__':
    single_main(build_prefix='extra-x86_64')
