"""Best-effort UI walkthrough on the emulator using adb + uiautomator: onboarding -> Home -> add a task."""
import re, subprocess, sys, time
def adb(*a): return subprocess.run(["adb", *a], capture_output=True, text=True).stdout
def dump():
    adb("shell", "uiautomator", "dump", "/sdcard/ui.xml"); return adb("shell", "cat", "/sdcard/ui.xml")
def find(xml, needle):
    for m in re.finditer(r"<node[^>]*>", xml):
        n = m.group(0); t = re.search(r'\btext="([^"]*)"', n); d = re.search(r'content-desc="([^"]*)"', n)
        if needle.lower() in ((t.group(1) if t else "") + "|" + (d.group(1) if d else "")).lower():
            b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', n)
            if b: x1, y1, x2, y2 = map(int, b.groups()); return (x1 + x2) // 2, (y1 + y2) // 2
    return None
def wait_for(needle, secs=25):
    end = time.time() + secs
    while time.time() < end:
        p = find(dump(), needle)
        if p: return p
        time.sleep(2)
    return None
def tap(p): adb("shell", "input", "tap", str(p[0]), str(p[1]))
failed = False
def step(name, ok, required=True):
    global failed; print(("PASS " if ok else ("FAIL " if required else "WARN ")) + name)
    if required and not ok: failed = True
    return ok
step("first screen shows TODO content", wait_for("Make Every Day Count") is not None)
for _ in range(3):                                   # swipe through the intro with the Next button
    p = find(dump(), "Next")
    if p: tap(p); time.sleep(1.2)
p = wait_for("Get Started", 8)
if p: tap(p)
step("Home appears after onboarding", wait_for("Priority focus", 15) is not None)
p = find(dump(), "New task")
if step("add-task button is visible", p is not None, required=False):
    tap(p); f = wait_for("What needs doing", 10)
    if step("quick-add sheet opens", f is not None, required=False):
        tap(f); time.sleep(1); adb("shell", "input", "text", "Smoke%stask"); time.sleep(1)
        b = find(dump(), "Add task")
        if b: tap(b)
        step("new task appears on Home", wait_for("Smoke task", 10) is not None, required=False)
sys.exit(1 if failed else 0)
