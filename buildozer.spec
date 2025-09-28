[app]
title = Автотайпер
package.name = autotyper
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 2.0
requirements = python3,kivy,requests,android,pyjnius

orientation = portrait

# Разрешения для Android
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,CAMERA

# Настройки Android
android.api = 33
android.minapi = 21
android.sdk = 28
android.ndk = 25b

# Дополнительные настройки
android.allow_backup = true

# Ключ для подписи (debug)
android.accept_sdk_license = True

[buildozer]
warn_on_root = 0
log_level = 2

# Оптимизация для CI
log_level = 2
