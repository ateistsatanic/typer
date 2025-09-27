[app]
title = Автотайпер
package.name = autotyper
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 2.0
requirements = python3,kivy,requests,android,pyjnius

orientation = portrait

[buildozer]
log_level = 2

[app]
# Разрешения для Android
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,CAMERA

# Настройки Android
android.api = 33
android.minapi = 21
android.ndk = 25b

# Дополнительные настройки
android.allow_backup = True
android.gradle_dependencies = 
    implementation 'androidx.core:core:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.0'
    implementation 'com.google.android.material:material:1.8.0'

# Разрешить доступ к файлам
android.manifest_intent_filters = 
    <intent-filter>
        <action android:name="android.intent.action.PICK" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="image/*" />
    </intent-filter>
