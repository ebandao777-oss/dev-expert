#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PostToolUse hook (GLOBAL): 写 PHP 文件后做语法自检。

后端 php -l：本环境 php -l 对语法错误返回退出码 0（异常），但 stdout 明确含
"Parse error" / "Errors parsing"。故以【输出字符串】判定（非退出码），对真实项目路径可靠闭环。
hook 跑的是工作区内真实文件（非 tempfile），故输出判定稳定。
- 仅对 .php 文件生效。
- 非阻塞：发现语法错误时 exit 1（warning，回显 AI），不阻断已完成的写入。
- 其他故障（如 php 找不到）静默 exit 0，避免误报卡住工作。
"""
import sys
import os
import json
import subprocess

PHP = r"F:\BtSoft\php\85\php.exe"


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
    if not os.path.isfile(path):
        return 0

    try:
        r = subprocess.run(
            [PHP, "-l", path],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return 0

    out = (r.stdout or "") + (r.stderr or "")
    # 本环境 php -l 退出码对语法错误仍为 0（异常），但 stdout 含 Parse error 可靠。
    # 成功信息 "No syntax errors detected" 不含 "Parse error"，不会误判。
    if "Parse error" in out or "Errors parsing" in out:
        print("[LINT-FAIL] php -l 发现语法错误：")
        print(out.strip())
        return 1  # warning，回显给 AI
    return 0


if __name__ == "__main__":
    sys.exit(main())
