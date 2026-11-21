# TODO - audit report

Nothing in this report was compiled or run on a device/emulator by the author (the authoring sandbox has no Android SDK, emulator or internet). "Fixed" means the source was changed; "verified" is reserved for checks that were actually executed (see the checklist). The GitHub workflow performs the real build, unit tests and emulator smoke test.

## Problems found and fixed
| # | Area | Problem | Fix |
|---|------|---------|-----|
| 1 | Gradle | `app/build.gradle.kts` used `java.net.URL` / `HttpURLConnection`; in Kotlin DSL `java` resolves to the Gradle Java extension, so this is an unresolved-reference build error (the "Java network imports" error) | Removed all network code from Gradle. The optional font download is now a `curl` step in the workflow |
| 2 | Black screen | Whole UI was drawn through a recorded GraphicsLayer (blur). If it records at the wrong size nothing is drawn; onboarding has no nav bar, so the first launch was fully black | Removed the layer and all dead backdrop code (`Backdrop.kt`, `LocalBackdrop`, glass `backdrop` parameter) |
| 3 | Startup | Possible blank screen while settings load / DataStore stalls | Visible splash, 1.5 s cap on waiting, DataStore read errors fall back to defaults, light/dark colours set before first frame, theme window background |
| 4 | Startup | Notification-permission dialog was launched on the first frame | Permission is now requested only when the user sets a reminder (Android 13+) |
| 5 | Data safety | Any Room error inside a coroutine/flow would crash the app | All reads (`catch`) and writes (`io {}` helper) log and continue; no destructive migration anywhere |
| 6 | Data | Two Room instances possible (VM + boot receiver) | `AppDb.get()` shared singleton |
| 7 | Reminders | Alarms are lost on reboot/app update | `BootReceiver` (BOOT_COMPLETED, MY_PACKAGE_REPLACED) re-arms all future reminders; `RECEIVE_BOOT_COMPLETED` declared. Time-zone changes need nothing: reminders are absolute instants and due dates are local dates |
| 8 | Recurring | Overdue repeating tasks produced copies that were already overdue; logic untestable | Extracted `nextOccurrence()` (pure), catches up to today, keeps reminders in the future; 8 JVM unit tests |
| 9 | Performance | Task filtering / grouping / chart maths ran on every recomposition; ticker woke 5x/s | `remember(keys)` for filters, Upcoming groups and Insights; 4x/s ticker |
| 10 | Accessibility | Chips ~34 dp tall, row delete 32 dp | 40 dp targets |
| 11 | Workflow | `tee` hid Gradle failures; no tests; fixed layout assumption | `pipefail`, layout auto-detect with a clear error, separate unit-test job, emulator smoke test with UI walkthrough, timeouts, evidence artifacts |
| 12 | Earlier errors | KSP `AppDb` MissingType, `Data.kt` missing brace, `fontFeatureSettings`, `Font()` constructor | Verified absent: braces balanced by comment-aware scan, no `fontFeatureSettings`/AssetManager `Font(...)` anywhere, font loader uses `Font(resId, weight)` after validating the resource |

## Known limitations (not fixed)
- `List<Task>` parameters are unstable for Compose, so some screens recompose more than strictly needed. A compiler stability option was not added because it cannot be verified offline.
- The Pomodoro timer keeps running only while the app process lives and does not notify at the end.
- Reminders are inexact (`setAndAllowWhileIdle`) on purpose (no exact-alarm permission); they can fire a few minutes late in Doze.
- Reminders use preset times only; no custom time picker.
- Room schema export and migration tests are not set up.
- Plus Jakarta Sans is downloaded at CI build time; if unavailable the system font is used.
