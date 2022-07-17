from lilaclib import *

def apply_patch(filename, patch):
    patch_proc = subprocess.Popen(["patch", "-p1", filename], stdin=subprocess.PIPE, text=True)
    patch_proc.communicate(patch)

def pre_build():
    _G.files = download_official_pkgbuild('caddy')

    # Apply patches
    apply_patch('PKGBUILD', PATCH)
    run_cmd(['sed', '-i','s/${pkgname}/${_pkgname}/g', 'PKGBUILD'])
    
    add_into_array('provides', ['${_pkgname}'])
    add_into_array('conflicts', ['${_pkgname}'])

    for line in edit_file('PKGBUILD'):
        if line.startswith('pkgname='):
            line = 'pkgname=caddy-cloudflare\n_pkgname=caddy'
        print(line)

def post_build():
    git_add_files(_G.files)
    git_commit()

PATCH=r'''
diff --git a/trunk/PKGBUILD b/trunk/PKGBUILD
index 8b195dd7..8c36253b 100644
--- a/trunk/PKGBUILD
+++ b/trunk/PKGBUILD
@@ -26,7 +26,8 @@ source=("git+https://github.com/caddyserver/caddy#tag=${_gitcommit}?signed"
         caddy.sysusers
         Caddyfile
         use-data-dir-for-autosave.patch
-        override-main-module-version.patch)
+        override-main-module-version.patch
+        plugin-cloudflare.patch)
 sha512sums=('SKIP'
             'SKIP'
             'b6f69b9818b1807ebd614f696f39ca2bacc58b748273d1122c2a96641093c2acf9e168ff6a2d5b2e8b2da073993b5245740d77975d4ca823ff0598675a6b7806'
@@ -35,7 +36,8 @@ sha512sums=('SKIP'
             'c893d88fec89e37da6596030c8dce7103e7e575371e8542a24d2a0741e877358d85219f2d8ade9d6aa0f515efe1156a4badd9fef5f65f553a5b0c72330c4728f'
             '716da3f4edeb3561243aeaf5c32b01ff7a4ac810b6deba8364fb12a1f71b6a5278c34a97b289bcfdc48784679b942bf780f1f36d416a575791168c94b0d59fe0'
             '563d6b45e91fc584fb5a27caaa382f59c140cb0a1b28b8d8faced4f7c7cad86d8671eb6ac10056f41518a842c8f606130d7e0c71df2b731d5eb0b4c868ea5d41'
-            'b06369dd976cfcc9b519782c088efa5fba25db61663112fcc4e20b108d5165cbebcf63b6fe6d1e36119a55271374bac0037a4d07af412241d6a4d2b4f4efda0b')
+            'b06369dd976cfcc9b519782c088efa5fba25db61663112fcc4e20b108d5165cbebcf63b6fe6d1e36119a55271374bac0037a4d07af412241d6a4d2b4f4efda0b'
+            '4af9af9023132e0f0645c9552c613135780c2e378e6a21513cc54adaef5e45e80f8c312c0832559aae0b38c00c26277d351dd178767977a3f6bfdab02aec7710')
 validpgpkeys=(
   29D0817A67156E4F25DC24782A349DD577D586A5 # Matthew Holt <mholt@users.noreply.github.com>
 )
@@ -55,6 +57,9 @@ prepare() {
   # fix version identifier if not built from a module
   patch -Np1 < "${srcdir}/override-main-module-version.patch"
   sed 's|"unknown"|"v'"${pkgver}"'"|g' -i caddy.go
+  # add custom plugins
+  patch -Np1 < "${srcdir}/plugin-cloudflare.patch"
+  go mod tidy -e
 }
 
 build() {

'''
if __name__ == '__main__':
    single_main(build_prefix='extra-x86_64')
