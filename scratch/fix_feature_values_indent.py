"""
fix_feature_values_indent.py
-----------------------------
Fixes the UnboundLocalError in ai_detector.py caused by
'feature_values' being incorrectly indented under a stray comment block.
"""
import pathlib, shutil

target = pathlib.Path("ai_detector.py")
shutil.copy(target, target.with_suffix(".py.bak2"))

src = target.read_text(encoding="utf-8")

# The broken block (note the 8-space indent on feature_values):
BAD = (
    "    # -- Feature details (for API transparency) --\r\n"
    "    \r\n"
    "        feature_values = extract_features_dict(text)\r\n"
)
GOOD = (
    "    # -- Feature details (for API transparency) --\r\n"
    "    feature_values = extract_features_dict(text)\r\n"
)

# Try CRLF first, then LF
if BAD in src:
    src = src.replace(BAD, GOOD, 1)
    print("[OK] Fixed CRLF version")
else:
    BAD_LF = BAD.replace("\r\n", "\n")
    GOOD_LF = GOOD.replace("\r\n", "\n")
    if BAD_LF in src:
        src = src.replace(BAD_LF, GOOD_LF, 1)
        print("[OK] Fixed LF version")
    else:
        # Fallback: search line by line
        lines = src.splitlines(keepends=True)
        fixed = []
        in_comment = False
        for line in lines:
            stripped = line.strip()
            if stripped == "# -- Feature details (for API transparency) --":
                in_comment = True
                fixed.append(line)
                continue
            if in_comment and stripped == "":
                # skip the blank spacer line from old patch
                in_comment = False
                continue
            if in_comment and "feature_values = extract_features_dict" in line:
                # Re-indent to 4 spaces
                fixed.append("    feature_values = extract_features_dict(text)\n")
                in_comment = False
                continue
            fixed.append(line)
        src = "".join(fixed)
        print("[OK] Fixed via line-by-line fallback")

target.write_text(src, encoding="utf-8")
print(f"Saved: {target} ({target.stat().st_size:,} bytes)")

# Verify syntax
import py_compile, tempfile, os
try:
    py_compile.compile(str(target), doraise=True)
    print("Syntax check: PASSED")
except py_compile.PyCompileError as e:
    print(f"Syntax check: FAILED - {e}")

# Verify fix applied
src2 = target.read_text(encoding="utf-8")
if "        feature_values" not in src2:
    print("Indent fix verified: no over-indented feature_values found")
else:
    print("WARNING: over-indented feature_values may still be present")
