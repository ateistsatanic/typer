[app]
title = Автотайпер v2.0
package.name = autotyper
package.domain = org.ateistsatanic

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 2.0
requirements = python3,kivy,requests,android

orientation = portrait

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23b

# Разрешаем доступ к хранилищу
android.gradle_dependencies = implementation 'androidx.core:core:1.6.0'

# Включаем все необходимые файлы
source.include_exts = py,png,jpg,kv,atlas,txt

[app]
# Настройки для сборки
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png