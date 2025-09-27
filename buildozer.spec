[app]
title = Автотайпер
package.name = autotyper
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0
requirements = python3,kivy,requests

orientation = portrait

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET
android.api = 30
android.minapi = 21
