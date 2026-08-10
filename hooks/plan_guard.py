#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PreToolUse hook (GLOBAL): 改核心目录前强制要求存在进行中 *_plan.md（对齐 Rules §13）。

- 仅对落在「核心/危险目录」的 .php 写操作拦截；tests/、Plan/、依赖/资源目录不拦。
- 拦截条件：目标在核心目录 且 其 workspace 的 Plan/ 下无任何状态为 规划中/进行中 的 *_plan.md。
- 命中 exit 2 阻断，提示先建计划（Trivial Fix 通道见 Rules §14，但核心目录改动仍强制规划）。
"""
import sys
import os
import json
import re

CORE_DIRS = {
    "e/class", "e/ebandao7890", "e/data", "e/config",
    "e/mods", "e/member", "e/template", "e/admin",
}
EXCLUDE_DIRS = {
    "tests", "Plan", "backup", "vendor", "node_modules",
    "uploads", ".codebuddy", "skin", "images", "d", "api", "search", "ecachefiles",
}

# 「## 状态」标题行（§13 模板为独占一行，状态值在同行或下一行）
HEAD_RE = re.compile(r'^##\s*状态\s*[:：]?$')


def find_workspace(path):
    """向上找含 Plan/ 子目录的祖先目录作为 workspace。"""
    d = os.path.dirname(path)
    while True:
        if os.path.isdir(os.path.join(d, "Plan")):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            return None
        d = nd


def has_active_plan(workspace):
    """Plan/*.md 中存在状态为 规划中/进行中 的计划即视为激活。

    状态值按实际格式落在「## 状态」同行或下一行（§13 模板为独占一行）。
    """
    plan_dir = os.path.join(workspace, "Plan")
    if not os.path.isdir(plan_dir):
        return False
    for fn in os.listdir(plan_dir):
        if not fn.endswith("_plan.md"):
            continue
        p = os.path.join(plan_dir, fn)
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if not HEAD_RE.match(line.strip()):
                continue
            # 同行或下一行含 规划中/进行中 即激活
            if re.search(r'(规划中|进行中)', line):
                return True
            if i + 1 < len(lines) and re.search(r'(规划中|进行中)', lines[i + 1]):
                return True
    return False


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        data = json.loads(raw)
    except Exception:
        return 0

    tool_input = data.get("tool_input", {}) or {}
    path = (
        tool_input.get("filePath")
        or tool_input.get("file_path")
        or tool_input.get("path")
        or ""
    )
    if not path:
        return 0
    path = os.path.abspath(path)
    if os.path.splitext(path)[1].lower() != ".php":
        return 0

    norm = path.replace("\\", "/").lower()
    parts = norm.split("/")
    # 排除非核心/资源/临时目录
    if any(part in EXCLUDE_DIRS for part in parts):
        return 0
    # 是否落在核心目录
    in_core = any(
        ("/%s/" % d) in norm or norm.endswith("/%s" % d) for d in CORE_DIRS
    )
    if not in_core:
        return 0

    workspace = find_workspace(path)
    if workspace is None:
        return 0  # 无 Plan 体系则不拦

    if has_active_plan(workspace):
        return 0

    print("[PLAN-GUARD] 拦截：改动核心目录前须先存在进行中的 *_plan.md（Rules §13）")
    print("目标: %s" % path)
    print("请在 Plan/ 下创建状态为「规划中/进行中」的 *_plan.md 后再改。")
    return 2  # 阻断


if __name__ == "__main__":
    sys.exit(main())
