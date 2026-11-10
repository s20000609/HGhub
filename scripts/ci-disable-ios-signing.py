#!/usr/bin/env python3
"""Disable code signing in the generated iOS Xcode project (CI, unsigned IPA)."""
import pathlib
import re

root = pathlib.Path("src-tauri/gen/apple")
extra = '    CODE_SIGNING_ALLOWED: "NO"\n    CODE_SIGNING_REQUIRED: "NO"\n    CODE_SIGN_IDENTITY: ""\n'

yml = root / "project.yml"
s = yml.read_text()
if re.search(r"^settings:\s*\n\s+base:\s*\n", s, re.M):
    s = re.sub(r"(^settings:\s*\n\s+base:\s*\n)", lambda m: m.group(1) + extra, s, count=1, flags=re.M)
else:
    s += "\nsettings:\n  base:\n" + extra
yml.write_text(s)

for pb in root.rglob("project.pbxproj"):
    t = pb.read_text()
    t = t.replace(
        "buildSettings = {",
        "buildSettings = {\n\t\t\t\tCODE_SIGNING_ALLOWED = NO;\n\t\t\t\tCODE_SIGNING_REQUIRED = NO;",
    )
    pb.write_text(t)
print("signing disabled")
