#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PreCompact hook (GLOBAL): 上下文压缩前写 ≤2KB 交接快照到 memory。

hook 拿不到对话内容，故快照基于文件系统派生（压缩后最实用的重定位信息）：
- 近 4 小时内被改动的项目文件（排除备份/依赖/缓存目录），按时间倒序取前 25
- 当前 Plan/*.md 的状态行（## 状态）
- 最新一份每日 memory 文件名
落点：<workspace>/.codebuddy/memory/_handoff_snapshot.md
（workspace 取 hook 运行 cwd；全局 hook 不写死单一项目路径）
"""
import sys
import os
import json
import time

CUTOFF_HOURS = 4
MAX_FILES = 25
EXCLUDE = {"backup", "vendor", "node_modules", "uploads",
           ".git", ".codebuddy", "ecachefiles"}


def main():
    try:
        sys.stdin.read()
    except Exception:
        pass

    root = os.getcwd()
    mem_dir = os.path.join(root, ".codebuddy", "memory")
    cutoff = time.time() - CUTOFF_HOURS * 3600

    recent = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d.lower() not in EXCLUDE and not d.startswith(".")]
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            try:
                mtime = os.path.getmtime(fp)
            except OSError:
                continue
            if mtime >= cutoff:
                recent.append((mtime, fp))
    recent.sort(reverse=True)
    recent = recent[:MAX_FILES]

    rel = lambda p: os.path.relpath(p, root).replace("\\", "/")
    lines = ["# 压缩交接快照 (PreCompact 自动生成)", ""]
    lines.append("生成时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("工作区: " + root)
    lines.append("")

    lines.append("## 近 %d 小时改动文件 (前 %d)" % (CUTOFF_HOURS, MAX_FILES))
    if recent:
        for mtime, fp in recent:
            lines.append("- %s  (%s)" % (rel(fp),
                                          time.strftime("%H:%M", time.localtime(mtime))))
    else:
        lines.append("- (无)")
    lines.append("")

    # Plan 状态
    lines.append("## 进行中计划 (Plan/*.md 状态)")
    plan_dir = os.path.join(root, "Plan")
    if os.path.isdir(plan_dir):
        for fn in sorted(os.listdir(plan_dir)):
            if not fn.endswith("_plan.md"):
                continue
            p = os.path.join(plan_dir, fn)
            status = ""
            try:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip().startswith("## 状态"):
                            status = line.strip()
                            break
            except OSError:
                pass
            lines.append("- %s  %s" % (fn, status))
    else:
        lines.append("- (无 Plan 目录)")
    lines.append("")

    # 最新 memory
    lines.append("## 最新记忆")
    if os.path.isdir(mem_dir):
        mds = [f for f in os.listdir(mem_dir) if f.endswith(".md")]
        mds.sort(reverse=True)
        if mds:
            lines.append("- 最新: .codebuddy/memory/%s" % mds[0])
        else:
            lines.append("- (无)")
    else:
        lines.append("- (无 memory 目录)")

    out = "\n".join(lines) + "\n"
    b = out.encode("utf-8")
    if len(b) > 2048:
        # 按字节截断并在字符边界安全解码，避免切断多字节中文
        b = b[:2048]
        out = b.decode("utf-8", errors="ignore")
    try:
        os.makedirs(mem_dir, exist_ok=True)
        snap = os.path.join(mem_dir, "_handoff_snapshot.md")
        tmp = snap + ".tmp"
        # 二进制写入：避免 Windows 文本模式把 \n 转 \r\n 撑大文件致超 2048
        with open(tmp, "wb") as f:
            f.write(out.encode("utf-8"))
        try:
            os.replace(tmp, snap)  # 原子替换，避免目标被读锁占用时写失败
        except OSError:
            # 极少数情况目标被锁：退回直接覆盖写
            with open(snap, "wb") as f:
                f.write(out.encode("utf-8"))
            try:
                os.remove(tmp)
            except OSError:
                pass
    except OSError:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
