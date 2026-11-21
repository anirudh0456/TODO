#!/bin/bash
# Installs the debug APK on the emulator, launches TODO, and fails if the app died, the screen is blank, or the UI walkthrough fails.
APK=$(ls app/build/outputs/apk/debug/app-debug.apk) || exit 1
adb wait-for-device
adb install -r "$APK" || exit 1
adb logcat -c
adb shell am start -W -n com.todo.app/.MainActivity
sleep 12
adb exec-out screencap -p > screenshot.png
if ! adb shell pidof com.todo.app > /dev/null; then echo "FAIL: app is not running (crashed)"; adb logcat -d > logcat.txt; grep -A25 "FATAL EXCEPTION" logcat.txt | head -60; exit 1; fi
STATUS=0
python3 ci/check_screenshot.py screenshot.png || STATUS=1
python3 ci/ui_smoke.py || STATUS=1
adb exec-out screencap -p > screenshot2.png
adb logcat -d > logcat.txt
if grep -q "FATAL EXCEPTION" logcat.txt; then echo "FAIL: crash found in logcat"; grep -A25 "FATAL EXCEPTION" logcat.txt | head -60; STATUS=1; fi
exit $STATUS
