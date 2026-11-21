# TODO (com.todo.app)

## Build the APK on GitHub
1. Create a repository and upload the CONTENTS of this folder (settings.gradle.kts, app/, ci/, .github/ ...), or upload the whole unzipped package (TODO folder + .github folder). The workflow finds the project either way.
2. Actions -> "Build TODO APK" -> Run workflow.
3. Download "TODO-debug-apk" (app-debug.apk) from the run Artifacts and install it.
4. Other jobs: "unit-tests" (JVM tests) and "smoke-test" (Android 14 emulator: launch, not-black check, onboarding -> Home -> add task; screenshots + logcat in "smoke-test-evidence"). They are independent of the APK: if one fails the APK is still valid. Send me the log if one fails.

See AUDIT-REPORT.md for everything found and fixed, and what is unverified. Nothing was compiled or run by the author.
