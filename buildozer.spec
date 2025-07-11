[app]

# (str) Title of your application
title = LeoBrooklyn

# (str) Package name
package.name = leobrooklyn

# (str) Package domain (used for Android package name)
package.domain = org.leobrooklyn

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,pygame

# (str) Main application file
main.py = main.py

# (list) Source files to include (relative to the Buildozer spec file)
source.include_exts = py,png,jpg,kv,atlas,ogg,mp3,ttf,json

# (list) List of inclusions using pattern matching
# Example: include_patterns = images/*.png,data/*.json
include_patterns = images/*,sounds/*

# (str) Kivy version to use
# If this is empty, the latest stable version will be used.
#kivy.version = 1.9.1

# (int) Android API level to use
android.api = 27

# (int) Android SDK version to use
android.sdk = 27

# (int) Android NDK version to use
android.ndk = 21b

# (bool) Enable Android debugging
android.debug = True

# (list) Android permissions
android.permissions = INTERNET

# (list) Android archs to build for
android.archs = arm64-v8a,armeabi-v7a

# (str) Path to the Android NDK directory
#android.ndk_path = /opt/android-ndk-r21b

# (str) Path to the Android SDK directory
#android.sdk_path = /opt/android-sdk

# (str) Path to the Java JDK directory
#android.jdk_path = /usr/lib/jvm/java-8-openjdk-amd64

[buildozer]

# (int) Log level (0 = error, 1 = warn, 2 = info, 3 = debug)
log_level = 2