#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_graph.py — dev-expert 项目知识图谱构建/查询工具

设计目标：
  - 工具侧正则抽取，输出写盘 {root}/.ai-memory/knowledge-graph/{graph.json,meta.json,symbols.json,graph.md}，不进 LLM 上下文（构建 token ≈ 0）。
  - 边类型：include/use/autoload/extends/template/tpimport/import/cssimport/asset/calls。
    跨语言抽取：PHP include/require + define() 常量链（含 ABSPATH.WPINC 等）、命名空间 use/extends、
    非 PHP（py/js/ts/java）模块导入、CSS @import、HTML link/script 资源、ThinkPHP import()/vendor()/Loader::import()、
    composer PSR-4/PSR-0 命名空间映射（fqn_to_file）、模板 {include file=}。
  - 存储结构见上；graph.md 为人类可读兜底（agent 不加载）。
  - 查询：--query <file|symbol> [--direction up|down|both] [--depth N] 返回裁剪子图（默认 2 跳，MAX_NODES=80 封顶）。
    注：--query 入口会先比对 mtime+内容哈希做新鲜度检测，过期则 [GRAPH-STALE] 并全量重建（v1 无独立增量逻辑，增量=全量重抽）。
  - 冷启动：图不存在 → 当场全量构建。
  - 环检测：遍历维护 visited，遇环折叠标 cycle（环边引用的祖先节点一并补入子图，见 B-2）。
  - 悬空边：构建时 add_edge_if_exists 对目标不存在/项目外绝对路径的边不进图，仅记入 meta.dangling_edges（非事后反查）。
  - accuracy_report：edges_valid（已存在目标）/edges_dangling/include_total/include_valid/static_coverage(include 解析率) 等。
    注：符号孤儿检测当前为占位（orphan_symbols 恒空），未实现"孤儿告警"，留口。
  - LSP 探测（detect_lsp）：仅 shutil.which('intelephense'/'phpactor') 探测 PHP 可用性并记 lsp_available；
    其余语言（js/python/java/go）硬编码 False。LSP 仅记录可用性，抽取仍走正则（可选增强留口）。
  - 纯 v1 正则实现（无 AST/tree-sitter）。
"""
import argparse
import hashlib
import json
import os
import re
import sys

# ---------- 默认排除目录（规划 §5.6 #7） ----------
EXCLUDE_DIRS = {
    # 依赖/构建产物
    'vendor', 'node_modules', 'dist', 'build', '__pycache__', '.cache',
    # 版本控制（避免抽 .git/.hg/.svn 内部文件）
    '.git', '.hg', '.svn',
    # 图谱产物自身（避免自引用重遍历）
    '.ai-memory',
    # 各 IDE / 编辑器项目级元数据目录
    '.codebuddy',   # CodeBuddy
    '.vscode',      # VS Code
    '.idea',        # JetBrains
    '.claude',      # Claude Code
    '.cursor',      # Cursor
    '.zed',         # Zed
    '.fleet',       # JetBrains Fleet
    '.sublime',     # Sublime Text
    # 国内 AI IDE
    '.trae',        # Trae
    '.qoder',       # Qoder / 通义灵码
    # 其他主流 IDE
    '.windsurf',    # Windsurf
    '.codeium',     # Codeium
    '.atom',        # Atom
    '.brackets',    # Brackets
    '.vs',          # Visual Studio
    '.metadata',    # Eclipse
    '.settings',    # Eclipse
    '.gradle',      # Gradle
    'nbproject',    # NetBeans
    'target',       # Maven / Eclipse 构建产物
}

# ---------- 纳入图谱的源码扩展名（遍历与新鲜度检测须一致） ----------
SRC_EXTS = ('.php', '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx',
            '.py', '.java', '.htm', '.html', '.css', '.scss', '.less')

# ---------- 抽取正则（PHP/JS，v1 一等支持） ----------
RE_REQ_STMT = re.compile(r"(?:require|include)(?:_once)?\s*\(?\s*(.+?)\s*\)?\s*;", re.I | re.S)
RE_STR = re.compile(r"['\"]([^'\"]+)['\"]")
RE_DYNAMIC_MARK = re.compile(r"\$\w+")  # 变量拼路径（如 $base . '/x'）→ 抽不出
RE_CLASS = [
    re.compile(r"(?:class|interface|trait|enum)\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w\s,]+))?"),
    re.compile(r"(?:public\s+|private\s+|protected\s+)?function\s+(\w+)\s*\("),
]
# ---------- 命名空间 / use（覆盖 composer PSR-4 框架：ThinkPHP/易优/迅睿/FastAdmin/Laravel） ----------
RE_NAMESPACE = re.compile(r"^\s*namespace\s+([\w\\]+)\s*;", re.M)
RE_USE = re.compile(r"^\s*use\s+([\w\\]+)(?:\s+as\s+(\w+))?\s*;", re.M)
RE_NEW_FQN = re.compile(r"new\s+\\?([\w\\]+)\s*\(")            # new \App\X 或 new App\X
RE_FQN_CALL = re.compile(r"\\?([\w\\]+)::")                     # \App\X::method
# ---------- 非 PHP 语言模块导入（覆盖 Django/Flask/Spring/Express/NestJS/Next/React/Vue/Angular/Strapi） ----------
RE_PY_IMPORT = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import\s+\w+|import\s+([\w.]+))", re.M)
RE_JS_REQUIRE = re.compile(r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
RE_JS_IMPORT = re.compile(r"import\s+(?:[^'\"(]*?\s+from\s+)?['\"]([^'\"]+)['\"]")
RE_JS_DYNAMIC_IMPORT = re.compile(r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
RE_JAVA_IMPORT = re.compile(r"^\s*import\s+(?:static\s+)?([\w.]+)\s*;", re.M)
RE_JAVA_PKG = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.M)
# ---------- ThinkPHP 显式类库导入（TP3/TP5 官方机制，thinkphp.cn/info/126） ----------
RE_TP_IMPORT = re.compile(r"(import|vendor|Loader::import)\s*\(\s*['\"]([^'\"]+)['\"]")


RE_TPL_INCLUDE = re.compile(
    r"\{\s*[a-z]*:?include\b[^}]*?\bfile\s*=\s*['\"]([^'\"]+)['\"]", re.I)
RE_TPL_REQUIRE = re.compile(r"template\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")  # template('x')
# ---------- CSS / HTML 资源依赖（前端样式与脚本依赖） ----------
RE_CSS_IMPORT = re.compile(r"@import\s+(?:url\()?\s*['\"]?([^'\"()\s;]+)['\"]?\s*\)?\s*;", re.I)
RE_HTML_LINK = re.compile(r"<link\b[^>]*\bhref\s*=\s*['\"]([^'\"]+)['\"]", re.I)
RE_HTML_SCRIPT = re.compile(r"<script\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"]", re.I)




def _resolve_const_include(head, lit, rel, const_table, root):
    """解析 require 表达式里的常量前缀拼接：CONST . 'lit' / CONST.CONST . 'lit' / 纯 CONST。

    D-1 提取自 extract_includes 内联块（语义 1:1 保留）：逐 token 调 resolve_const 解析常量值，
    路径段间用斜杠拼接（base.rstrip('/') + '/' + rb.lstrip('/')），最后做绝对/相对归一。
    返回相对 root 的 rel 字符串；常量未定义/循环/含变量 → None（交由调用方落字面量兜底）。
    注意：不使用 _resolve_const_rhs（其路径段拼接不加斜杠，对多常量链会丢失分隔符）。
    """
    lit = lit or ''
    base = ''
    ok = True
    if re.match(r"^[A-Z_][A-Z0-9_]*$", head):
        base = resolve_const(head, const_table, root) if head in const_table else None
        if base is None:
            ok = False
    else:  # 常量链 CONST . CONST . ...
        for tok in re.split(r"\s*\.\s*", head):
            rb = resolve_const(tok, const_table, root) if tok in const_table else None
            if rb is None:
                ok = False
                break
            base = (base.rstrip('/') + '/' + rb.lstrip('/')) if base else rb
    if not ok:
        return None
    base = os.path.normpath(base) if base else ''
    if lit:
        lit2 = lit.lstrip('/')
        if base and (base.startswith('/') or re.match(r'^[A-Za-z]:', base) or os.path.isabs(base)):
            target = os.path.normpath(base.rstrip('/') + '/' + lit2)
        else:
            target = os.path.normpath(os.path.join(base, lit2)) if base else os.path.normpath(lit2)
    else:
        target = base
    if base and not (target.startswith('/') or re.match(r'^[A-Za-z]:', target) or os.path.isabs(target)):
        target = os.path.normpath(os.path.join(root, target))
    return target


def strip_php_comments(text):
    """B2：抽取 include 前剥离 PHP 注释，避免 `// include('x')` 这类注释/死代码被当真边。

    启发式（纯静态，非解析器）：先去块状 `/* ... */`，再按行处理行注释 `//`/`#`——
    仅当行注释符前为行首空白或语句结束符(`;`/`}`/`{`/`)`)时才视为注释，降低误伤
    字符串内 `http://`、`"#"` 等同行合法 require 的概率。已知局限：字符串内注释符仍可能误剥。
    """
    # 1) 去块注释
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out = []
    for line in text.split('\n'):
        # 找行注释起点：遍历字符，遇未闭合引号内的 // # 跳过
        in_s = False
        quote = ''
        i = 0
        n = len(line)
        cut = -1
        while i < n:
            ch = line[i]
            if in_s:
                if ch == '\\':
                    i += 2
                    continue
                if ch == quote:
                    in_s = False
            else:
                if ch in ('"', "'"):
                    in_s = True
                    quote = ch
                elif ch == '#':
                    cut = i
                    break
                elif ch == '/' and i + 1 < n and line[i + 1] == '/':
                    cut = i
                    break
            i += 1
        if cut >= 0:
            # 行注释符前需为行首空白或语句结束符，否则视为字符串/URL 内
            head = line[:cut].rstrip()
            if head == '' or head.endswith((';', '}', '{', ')', '?')):
                out.append(line[:cut])
                continue
        out.append(line)
    return '\n'.join(out)


def extract_includes(text, rel, root, const_table=None):
    """提取 include/require 目标。

    支持四类写法（覆盖国内帝国/易优/迅睿/ThinkPHP 等 CMS 与框架）：
      1) 字面量 / ./ ../ 相对路径
      2) __DIR__ / dirname(__FILE__) 拼接
      3) define() 常量前缀拼接：CONST 或 CONST . 'lit'（递归解析常量 RHS）
      4) 变量拼路径（$base . '/x'）→ 动态，抽不出，跳过（规划漏抽边界）
    常量被引用但无法静态解析（未定义/循环/含变量）→ 跳过，避免误边。
    B2：PHP 文件抽取前先剥离注释，避免注释/死代码里的 include 被当成真实依赖边。
    """
    text = strip_php_comments(text)
    const_table = const_table or {}
    includes = []
    for m in RE_REQ_STMT.finditer(text):
        expr = m.group(1).strip()
        # 1) __DIR__ / dirname(...) 拼接（保持原行为）
        if '__DIR__' in expr or 'dirname(' in expr:
            sm = RE_STR.search(expr)
            if sm:
                raw = sm.group(1)
                target = os.path.normpath(os.path.join(os.path.dirname(rel), raw.lstrip('/')))
                includes.append(target)
            continue
        # 2) define() 常量前缀拼接：CONST . 'lit' / CONST.CONST . 'lit' 链 / 纯 CONST
        # D-1 去重：原内联常量链拼接块较长且易与 resolve_const 混淆，现提取为独立函数
        # _resolve_const_include（语义 1:1 保留：逐 token 调 resolve_const + 路径段斜杠拼接 +
        # 绝对/相对归一）。注意刻意不复用 _resolve_const_rhs：后者路径段拼接不加斜杠，
        # 对多常量链（A.B）会产生 e/asubx.php 错误路径，故 require 表达式解析独立维护。
        cm = re.match(
            r"^((?:[A-Z_][A-Z0-9_]*)(?:\s*\.\s*[A-Z_][A-Z0-9_]*)*)"
            r"\s*\.\s*['\"]([^'\"]*)['\"]$", expr) or \
            re.match(r"^([A-Z_][A-Z0-9_]*)$", expr)
        if cm:
            target = _resolve_const_include(cm.group(1),
                                            cm.group(2) if len(cm.groups()) >= 2 else '',
                                            rel, const_table, root)
            if target is not None:
                includes.append(target)
                continue
            # 常量未定义或无法静态解析 → 落到下方字面量兜底（旧行为），不跳过
        # 3) 字面量 / 相对路径（原逻辑）
        sm = RE_STR.search(expr)
        if not sm:
            continue
        raw = sm.group(1)
        # 变量拼路径（如 $base . '/x'）→ 动态，正则抽不出，跳过（规划漏抽边界）
        if RE_DYNAMIC_MARK.search(expr):
            continue
        if raw.startswith('/') or re.match(r'^[A-Za-z]:', raw):
            target = os.path.normpath(raw)
        elif raw.startswith('./') or raw.startswith('../'):
            target = os.path.normpath(os.path.join(os.path.dirname(rel), raw))
        else:
            # 无前缀 include_path 风格，回退 root
            target = os.path.normpath(os.path.join(os.path.dirname(rel), raw))
            if not os.path.exists(target):
                target = os.path.normpath(os.path.join(root, raw))
        includes.append(target)
    return includes


def file_hash(path):
    """返回文件 md5；无读权限/不存在等异常返回 None（B4：避免 need_rebuild/build 因单文件不可读而整体崩溃）。"""
    try:
        h = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _safe_mtime(path):
    """返回文件 mtime；异常返回 None（need_rebuild 的廉价新鲜度前置过滤用）。"""
    try:
        return os.path.getmtime(path)
    except Exception:
        return None


def detect_lsp(root):
    """规划 §5.1 运行时 LSP 探测（仅记录可用性，v1 抽取仍走正则）。"""
    import shutil
    avail = {}
    # D-2：统一用 shutil.which 探测，移除跨平台脆弱的 os.system('npm ls -g ... >nul') 同步阻塞调用。
    # 全局 npm 装的 intelephense 不在 PATH 时 which 找不到 → False（仅可用性记录，抽取仍走正则，无功能影响）。
    try:
        avail['php'] = bool(shutil.which('intelephense') or shutil.which('phpactor'))
    except Exception:
        avail['php'] = False
    # 其他语言默认 False（本机实测）
    for lang in ('js', 'python', 'java', 'go'):
        avail[lang] = False
    return avail


# ---------- define() 常量前缀解析（覆盖国内 CMS/框架） ----------
RE_DEFINE = re.compile(
    r"define\s*\(\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*,\s*(.+?)\s*\)\s*;",
    re.I | re.S)
RE_CONST_DECL = re.compile(
    r"(?:public\s+|private\s+|protected\s+|final\s+|static\s+)*"
    r"const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([^;]+?)\s*;", re.I)


def extract_defines(text, rel):
    """抽取本文件 define()/const 常量 -> {NAME: (raw_rhs, defining_rel)}。"""
    out = {}
    for m in RE_DEFINE.finditer(text):
        out[m.group(1)] = (m.group(2).strip(), rel)
    for m in RE_CONST_DECL.finditer(text):
        out[m.group(1)] = (m.group(2).strip(), rel)
    return out


def _resolve_segment(seg, const_table, root, seen):
    """解析单个拼接段：字面量 / dirname() / 裸常量名。无法静态解析返回 None。"""
    seg = seg.strip()
    if not seg:
        return ''
    sm = re.match(r"^['\"]([^'\"]*)['\"]$", seg)
    if sm:
        return sm.group(1)
    dm = re.match(r"^dirname\(\s*(.*?)\s*\)$", seg)
    if dm:
        inner = _resolve_segment(dm.group(1), const_table, root, seen)
        if inner is None:
            return None
        return os.path.dirname(inner)
    if re.match(r"^[A-Z_][A-Z0-9_]*$", seg):
        return resolve_const(seg, const_table, root, seen)
    return None  # 含 $ / 函数调用等无法静态解析


def _resolve_const_rhs(raw, defining_rel, const_table, root, seen):
    """解析常量 RHS：字面量 / . 拼接链；__DIR__/__FILE__ 用 defining_rel 替换。"""
    raw = raw.strip()
    sm = re.match(r"^['\"]([^'\"]*)['\"]$", raw)
    if sm:
        return sm.group(1)
    work = raw
    if '__DIR__' in work:
        work = work.replace('__DIR__',
                            "'" + os.path.normpath(os.path.join(root,
                                os.path.dirname(defining_rel))).replace(os.sep, '/') + "'")
    if '__FILE__' in work:
        work = work.replace('__FILE__',
                            "'" + os.path.normpath(os.path.join(root,
                                defining_rel)).replace(os.sep, '/') + "'")
    # 按 ` . `（带空格的拼接运算符）切分，避免误切字符串内的点（如 .php）
    parts = re.split(r"\s+\.\s+", work)
    res = ''
    for p in parts:
        if p.strip() == '':
            continue
        seg = _resolve_segment(p, const_table, root, seen)
        if seg is None:
            return None
        res += seg
    if res:
        res = os.path.normpath(res)
        # 解析结果若落在 root 内（绝对），转回相对路径，保持图谱可移植
        if os.path.isabs(res) and res.startswith(os.path.abspath(root)):
            res = os.path.relpath(res, os.path.abspath(root)).replace(os.sep, '/')
            if res == '.':
                res = ''  # 解析结果恰为项目根 → 空串，避免拼接出 '.extend' 这类错误路径
        return res
    return None


def resolve_const(name, const_table, root, seen=None):
    """递归解析一个 define 常量的值为真实路径片段；循环/未定义/含变量返回 None。"""
    if seen is None:
        seen = set()
    if name in seen:
        return None
    entry = const_table.get(name)
    if not entry:
        return None
    raw, drel = entry
    seen.add(name)
    return _resolve_const_rhs(raw, drel, const_table, root, seen)


def parse_composer(root):
    """解析 composer.json 的 autoload（psr-4 / psr-0 / files / classmap）。

    返回 {psr4: {prefix: dir}, psr0: {prefix: dir}, files: [rel...], classmap: [dir...]}。
    国内 ThinkPHP/易优/迅睿/FastAdmin/Laravel 等框架靠此把命名空间映射到文件。
    """
    out = {'psr4': {}, 'psr0': {}, 'files': [], 'classmap': []}
    cj = os.path.join(root, 'composer.json')
    if not os.path.isfile(cj):
        return out
    try:
        data = json.load(open(cj, encoding='utf-8', errors='ignore'))
    except Exception:
        return out
    al = data.get('autoload', {})
    for kind, key in (('psr4', 'psr-4'), ('psr0', 'psr-0')):
        for pref, d in (al.get(key) or {}).items():
            pref = pref.rstrip('/').rstrip('\\')  # A-1：剥离 PSR-4/PSR-0 前缀尾部反斜杠，使 fqn_to_file 的 pref+'\\' 拼接正确命中
            # PSR-4/PSR-0 标准前缀尾部反斜杠（如 "App\\": "app/"）须剥离，
            # 否则 fqn_to_file 的 pref+'\\' 拼接会多一个反斜杠导致 startswith 永 False（A-1）
            if isinstance(d, list):
                for x in d:
                    out[kind][pref] = x.rstrip('/').rstrip('\\')
            else:
                out[kind][pref] = d.rstrip('/').rstrip('\\')
    for f in (al.get('files') or []):
        out['files'].append(f)
    for cm in (al.get('classmap') or []):
        out['classmap'].append(cm)
    return out


def fqn_to_file(fqn, composer, root):
    """按 PSR-4 / PSR-0 把完全限定类名映射到文件路径；找不到返回 None。"""
    fqn = fqn.lstrip('\\')
    parts = fqn.split('\\')
    # PSR-4：最长前缀匹配
    for pref in sorted(composer['psr4'], key=len, reverse=True):
        if fqn == pref or fqn.startswith(pref + '\\'):
            rest = fqn[len(pref):].lstrip('\\').split('\\')
            d = composer['psr4'][pref]
            rel = os.path.normpath(os.path.join(d, *rest)) + '.php'
            if os.path.isfile(os.path.join(root, rel)):
                return rel.replace(os.sep, '/')
            return rel.replace(os.sep, '/')  # 即便文件暂缺也返回预期路径（标悬空）
    # PSR-0：每段映射
    for pref in sorted(composer['psr0'], key=len, reverse=True):
        if fqn == pref or fqn.startswith(pref + '\\'):
            rest = fqn[len(pref):].lstrip('\\').split('\\')
            d = composer['psr0'][pref]
            rel = os.path.normpath(os.path.join(d, *rest)) + '.php'
            if os.path.isfile(os.path.join(root, rel)):
                return rel.replace(os.sep, '/')
            return rel.replace(os.sep, '/')
    return None


def resolve_module(spec, lang, rel, root):
    """按语言把 import 模块说明符解析为项目内文件 rel（或 None）。

    覆盖：Python import/from、JS CommonJS require + ESM import、Java import。
    相对路径(. / ..)优先相对源文件；裸说明符回退 node_modules / 包根启发式。
    """
    spec = spec.strip()
    if not spec:
        return None
    # rel 在 Windows 下是 '/' 分隔，os.path.dirname 不认 '/'，须转成本地分隔符
    rel_native = rel.replace('/', os.sep)
    src_dir = os.path.dirname(rel_native)
    src_full = os.path.join(root, src_dir) if src_dir else root
    if lang == 'py':
        parts = spec.split('.')
        if parts and parts[0] == '':
            parts = parts[1:]  # 去前导点（.models）
        cands = []
        for base in (src_full, root):
            cands.append(os.path.join(base, *parts) + '.py')
            cands.append(os.path.join(base, *parts, '__init__.py'))
        for c in cands:
            if os.path.isfile(c):
                return os.path.relpath(c, root).replace(os.sep, '/')
        return None
    if lang in ('js', 'ts'):
        if spec.startswith('./') or spec.startswith('../'):
            base = os.path.normpath(os.path.join(src_full, spec))
            # 若说明符自身已带扩展名（./styles.css），优先按原样试
            if os.path.splitext(spec)[1]:
                if os.path.isfile(base):
                    return os.path.relpath(base, root).replace(os.sep, '/')
            for ext in ('.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs', '.json', '.css', '.scss', '.less'):
                c = base + ext
                if os.path.isfile(c):
                    return os.path.relpath(c, root).replace(os.sep, '/')
            for idx in ('index.js', 'index.ts', 'index.jsx', 'index.tsx'):
                c = os.path.join(base, idx)
                if os.path.isfile(c):
                    return os.path.relpath(c, root).replace(os.sep, '/')
            return None
        # 裸说明符：node_modules 启发式
        nm_dirs = [os.path.join(root, 'node_modules')]
        if src_dir:
            nm_dirs.append(os.path.join(root, src_dir, 'node_modules'))
        for nm in (spec, spec.lstrip('@')):
            for top in nm_dirs:
                c = os.path.join(top, nm)
                for entry in ('index.js', 'index.ts', 'index.jsx', 'index.tsx', 'src/index.js', 'src/index.ts'):
                    if os.path.isfile(os.path.join(c, entry)):
                        return os.path.relpath(os.path.join(c, entry), root).replace(os.sep, '/')
        return None
    if lang == 'java':
        parts = spec.split('.')
        rest = parts[:-1] if spec.endswith('.*') else parts
        relp = os.path.normpath(os.path.join(*rest)) + '.java'
        c = os.path.join(root, relp)
        if os.path.isfile(c):
            return os.path.relpath(c, root).replace(os.sep, '/')
        # 包路径相对源码根（com/x/Y.java 可能位于 root 下任意 java/ 子目录），递归搜索
        for dp, _, fns in os.walk(root):
            if any(x in dp for x in EXCLUDE_DIRS):
                continue
            cand = os.path.join(dp, relp)
            if os.path.isfile(cand):
                return os.path.relpath(cand, root).replace(os.sep, '/')
        return None
    return None


def resolve_tp_import(spec, root, const_table):
    """解析 ThinkPHP import()/vendor()/Loader::import()（官方规则 thinkphp.cn/info/126）。

    点号转目录；基库前缀映射（依赖项目定义的常量，经 resolve_const 解析）：
      Think.*   -> THINK_PATH/Lib/*           (去 Think 前缀，后缀 .class.php)
      ORG.*     -> EXTEND_PATH/Library/ORG/*  (保留 ORG 段，后缀 .class.php)
      Com.*     -> EXTEND_PATH/Library/Com/*  (保留 Com 段，后缀 .class.php)
      Vendor.*  -> VENDOR_PATH/*              (去 Vendor 前缀；vendor() 调用已补 Vendor.)
      @.*       -> APP_PATH/*                 (去 @ 前缀，后缀 .class.php)
      其它(项目类库,如 Common.Tool/MyApp.Action.User) -> APP_PATH/* 完整点路径
        (.class.php 优先，缺失回退 .php，覆盖 import('X', APP_PATH, '.php') 形态)
    别名导入(单段无点,如 import('rbac')) 需 alias.php 映射,静态难穷举,留口 None。
    """
    spec = spec.strip()
    if not spec or '.' not in spec:
        return None  # 别名/多参仅首参带点形式留口
    parts = spec.split('.')
    head = parts[0]
    if spec.startswith('@'):
        base = resolve_const('APP_PATH', const_table, root) or 'application'
        parts = parts[1:]                      # 去 @ 别名段
        suffix = '.class.php'
    elif head == 'Think':
        tp = resolve_const('THINK_PATH', const_table, root) or \
            resolve_const('LIB_PATH', const_table, root) or 'ThinkPHP'
        base = (tp.rstrip('/') + '/Lib') if tp else 'ThinkPHP/Lib'
        parts = parts[1:]                      # 去 Think 前缀
        suffix = '.class.php'
    elif head in ('ORG', 'Com'):
        ep = resolve_const('EXTEND_PATH', const_table, root) or 'Extend/Library'
        base = (ep.rstrip('/') + '/Library') if ep else 'Extend/Library'
        # 保留 ORG/Com 段（EXTEND_PATH/Library/ORG/...）；用首段精确匹配避免 Common 误命中 Com
        suffix = '.class.php'
    elif head == 'Vendor':
        vp = resolve_const('VENDOR_PATH', const_table, root) or 'Vendor'
        base = vp.rstrip('/') if vp else 'Vendor'
        parts = parts[1:]                      # 去 Vendor 前缀（base 已是 VENDOR_PATH）
        suffix = '.class.php'
    else:  # 项目/应用类库：完整点路径映射目录（Common.Tool 不会误命中 Com 前缀）
        base = resolve_const('APP_PATH', const_table, root) or 'application'
        suffix = '.class.php'
    if not base or not parts:
        return None
    relp = os.path.normpath(os.path.join(base, *parts)) + suffix
    c = os.path.join(root, relp)
    if os.path.isfile(c):
        return os.path.relpath(c, root).replace(os.sep, '/')
    # 项目类库非标准后缀回退 .php（import('X', APP_PATH, '.php') 形态）
    if suffix == '.class.php':
        c2 = os.path.join(root, os.path.normpath(os.path.join(base, *parts)) + '.php')
        if os.path.isfile(c2):
            return os.path.relpath(c2, root).replace(os.sep, '/')
    return None


def extract_file(path, root, const_table=None):
    """抽取单文件：返回 {includes, classes, calls, namespace, uses, tpl_includes}。"""
    text = ''
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except Exception:
        return {'includes': [], 'classes': [], 'calls': [], 'namespace': None,
                'uses': [], 'tpl_includes': []}
    rel = os.path.relpath(path, root).replace(os.sep, '/')
    # include/require 是 PHP 专属语法（include(_once)/require(_once)）；其余语言（JS/TS/Java/Py/CSS/HTML）
    # 走各自的模块导入机制，禁止用 PHP 正则误抽，否则 JS 中 `src:`/`require()` 等会被当成 include 噪声边。
    PHP_EXTS = ('.php', '.inc', '.phtml', '.php3', '.php4', '.php5')
    includes = extract_includes(text, rel, root, const_table) if rel.endswith(PHP_EXTS) else []
    # 命名空间：取第一个文件级 namespace（复合文件取首个）
    ns_m = RE_NAMESPACE.search(text)
    namespace = ns_m.group(1) if ns_m else None
    # use 导入
    uses = [{'fqn': m.group(1), 'alias': m.group(2)} for m in RE_USE.finditer(text)]
    classes = []
    for m in RE_CLASS[0].finditer(text):
        cls = m.group(1)
        ext = m.group(2)
        impl = m.group(3)
        classes.append({'name': cls, 'line': text[:m.start()].count('\n') + 1,
                        'extends': ext, 'implements': impl})
    funcs = []
    for m in RE_CLASS[1].finditer(text):
        funcs.append(m.group(1))
    # calls：new X() / X->method() / X::const（跨文件才记，规划 §4 敏感边约束）
    calls = []
    for m in re.finditer(r"new\s+(\w+)\s*\(", text):
        calls.append(m.group(1))
    for m in re.finditer(r"(\w+)->\w+\s*\(", text):
        calls.append(m.group(1))
    for m in re.finditer(r"(\w+)::\w+", text):
        calls.append(m.group(1))
    # 模板 include 标签（帝国/Dede/Discuz/易优 模板依赖）
    tpl_includes = []
    for m in RE_TPL_INCLUDE.finditer(text):
        tpl_includes.append(m.group(1))
    for m in RE_TPL_REQUIRE.finditer(text):
        tpl_includes.append(m.group(1))
    # new \Ns\Class（框架类实例化，composer 自动加载）
    new_fqns = [m.group(1) for m in RE_NEW_FQN.finditer(text)]
    # ThinkPHP 显式类库导入 import()/vendor()/Loader::import()（TP3/TP5 官方机制）
    tp_imports = []
    if rel.endswith('.php'):
        for m in RE_TP_IMPORT.finditer(text):
            tp_imports.append((m.group(1), m.group(2)))
    # 非 PHP 语言模块导入（Django/Flask/Spring/React/Vue/...）
    lang = None
    if rel.endswith('.py'):
        lang = 'py'
    elif rel.endswith(('.js', '.jsx', '.mjs', '.cjs')):
        lang = 'js'
    elif rel.endswith(('.ts', '.tsx')):
        lang = 'ts'
    elif rel.endswith('.java'):
        lang = 'java'
    module_imports = []
    if lang == 'py':
        for m in RE_PY_IMPORT.finditer(text):
            module_imports.append(m.group(1) or m.group(2))
    elif lang in ('js', 'ts'):
        for m in RE_JS_REQUIRE.finditer(text):
            module_imports.append(m.group(1))
        for m in RE_JS_IMPORT.finditer(text):
            module_imports.append(m.group(1))
        for m in RE_JS_DYNAMIC_IMPORT.finditer(text):
            module_imports.append(m.group(1))
    elif lang == 'java':
        java_pkg = RE_JAVA_PKG.search(text)
        for m in RE_JAVA_IMPORT.finditer(text):
            module_imports.append(m.group(1))
    # CSS @import 依赖（指向其它样式文件，真实样式级联依赖）
    css_imports = []
    if rel.endswith(('.css', '.scss', '.less')):
        for m in RE_CSS_IMPORT.finditer(text):
            css_imports.append(m.group(1))
    # HTML <link href> / <script src> 资源依赖（样式表与脚本，排除图片等噪声）
    # .php 亦输出 HTML（CMS 模板普遍在 .php 中直接写 <link>/<script>）
    html_assets = []
    if rel.endswith(('.php', '.htm', '.html')):
        for m in RE_HTML_LINK.finditer(text):
            if m.group(1).endswith(('.css', '.scss', '.less', '.js', '.jsx',
                                     '.ts', '.tsx', '.mjs', '.cjs')):
                html_assets.append(m.group(1))
        for m in RE_HTML_SCRIPT.finditer(text):
            if m.group(1).endswith(('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs')):
                html_assets.append(m.group(1))
    return {'rel': rel, 'includes': includes, 'classes': classes,
            'funcs': funcs, 'calls': calls, 'namespace': namespace,
            'uses': uses, 'tpl_includes': tpl_includes, 'new_fqns': new_fqns,
            'lang': lang, 'module_imports': module_imports, 'tp_imports': tp_imports,
            'css_imports': css_imports, 'html_assets': html_assets}


def build(root):
    """全量构建。返回 (graph, meta, symbols)。"""
    out_dir = os.path.join(root, '.ai-memory', 'knowledge-graph')
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS
                       and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith(SRC_EXTS):
                files.append(os.path.join(dirpath, fn))
    file_list = [os.path.relpath(p, root).replace(os.sep, '/') for p in files]
    lsp = detect_lsp(root)
    # 常量预扫描（支持 define()/const 前缀拼路径的国内 CMS/框架）
    CONST_TABLE = {}
    for f, p in sorted(zip(file_list, files)):  # 常量预扫描按 rel 排序，避免同常量多定义时解析随遍历顺序漂移（B-1）
        try:
            txt = open(p, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        for nm, val in extract_defines(txt, f).items():
            CONST_TABLE[nm] = val  # 后定义覆盖
    extracted = {f: extract_file(p, root, CONST_TABLE) for f, p in zip(file_list, files)}
    COMPOSER = parse_composer(root)

    nodes = {}      # rel -> {type, classes, funcs}
    edges = []      # {from, to, kind}
    edge_keys = set()  # 边去重键集合（B-4）：(from, to, kind) 精确去重，避免重复 require 产生重复边
    symbols = {}    # name -> {file, line}
    fqn_symbols = {}  # FQN -> file（命名空间类，覆盖 composer 框架）
    dangling = []
    orphan_symbols = []
    include_total = 0
    include_valid = 0

    # 第一轮：建符号表（含命名空间 FQN）
    for rel, ex in extracted.items():
        ns = ex['namespace']
        for c in ex['classes']:
            symbols[c['name']] = {'file': rel, 'line': c['line']}
            if ns:
                fqn_symbols[(ns + '\\' + c['name']).lower()] = rel
        nodes[rel] = {'file': rel, 'classes': [c['name'] for c in ex['classes']],
                      'funcs': ex['funcs']}

    def add_edge_if_exists(rel, target_rel, kind, symbol=None):
        """已存在则加 include 边；否则记悬空（不进图）。"""
        nonlocal include_total, include_valid, edge_keys
        # define() 常量链解析可能产生项目内绝对路径 → 归一为相对 rel（保证图谱可移植、query 可遍历）
        if os.path.isabs(target_rel):
            normed = os.path.normpath(target_rel)  # 统一分隔符后再判项目内（Windows 下正斜杠/反斜杠）
            if normed.startswith(os.path.abspath(root)):
                target_rel = os.path.relpath(normed, os.path.abspath(root)).replace(os.sep, '/')
            else:
                return  # 项目外绝对路径，不纳入图谱
        if kind == 'include':
            include_total += 1
        if target_rel and os.path.exists(os.path.join(root, target_rel)):
            if any(d in target_rel.split('/') for d in EXCLUDE_DIRS):
                return
            if kind == 'include':
                include_valid += 1
            key = (rel, target_rel, kind)
            if key in edge_keys:
                return
            edge_keys.add(key)
            e = {'from': rel, 'to': target_rel, 'kind': kind}
            if symbol:
                e['symbol'] = symbol
            edges.append(e)
        else:
            dangling.append({'from': rel, 'raw': target_rel, 'resolved': target_rel,
                             'base': 'ns' if kind != 'include' else 'src'})

    for rel, ex in extracted.items():
        for c in ex['classes']:
            if c.get('extends'):
                ext = c['extends']
                # extends 可能是短名(同文件/全局)或 FQN
                tgt = None
                if '\\' in ext:
                    tgt = fqn_symbols.get(ext.lower()) or fqn_to_file(ext, COMPOSER, root)
                elif ext in symbols:
                    tgt = symbols[ext]['file']
                if tgt:
                    add_edge_if_exists(rel, tgt, 'extends')
        for inc in ex['includes']:
            add_edge_if_exists(rel, inc.replace(os.sep, '/'), 'include')
        # use 导入解析（composer PSR-4 框架核心机制）
        for u in ex['uses']:
            fqn = u['fqn']
            tgt = fqn_symbols.get(fqn.lower()) or fqn_to_file(fqn, COMPOSER, root)
            if tgt:
                add_edge_if_exists(rel, tgt, 'use', symbol=fqn)
        # new \Ns\Class / \Ns\Class:: （框架类实例化/静态调用）
        for fqn in ex['new_fqns']:
            tgt = fqn_symbols.get(fqn.lower()) or fqn_to_file(fqn, COMPOSER, root)
            if tgt and tgt != rel:
                add_edge_if_exists(rel, tgt, 'autoload', symbol=fqn)
        # ThinkPHP import()/vendor() 显式类库导入（TP3/TP5，官方 thinkphp.cn/info/126）
        for func, spec in ex['tp_imports']:
            if func == 'vendor':
                spec = 'Vendor.' + spec  # vendor() 说明符隐含 Vendor. 前缀
            tgt = resolve_tp_import(spec, root, CONST_TABLE)
            if tgt and tgt != rel:
                add_edge_if_exists(rel, tgt, 'tpimport', symbol=spec)
        # 非 PHP 语言模块导入（Django/Flask/Spring/React/Vue/Angular/Next/Nest/Strapi）
        if ex['lang']:
            for spec in ex['module_imports']:
                tgt = resolve_module(spec, ex['lang'], rel, root)
                if tgt and tgt != rel:
                    add_edge_if_exists(rel, tgt, 'import', symbol=spec)
        # 模板 {include file=}（帝国/Dede/Discuz/易优 模板依赖）
        for tpl in ex['tpl_includes']:
            trel = os.path.normpath(tpl.lstrip('/'))
            if not (trel.startswith('/') or re.match(r'^[A-Za-z]:', trel)):
                trel = os.path.normpath(os.path.join(os.path.dirname(rel), trel))
            add_edge_if_exists(rel, trel.replace(os.sep, '/'), 'template')
        # CSS @import 依赖（样式级联，指向其它样式文件）
        for imp in ex['css_imports']:
            trel = os.path.normpath(os.path.join(os.path.dirname(rel), imp.lstrip('/')))
            add_edge_if_exists(rel, trel.replace(os.sep, '/'), 'cssimport')
        # HTML <link href> / <script src> 资源依赖（样式表与脚本）
        for a in ex['html_assets']:
            if a.startswith(('/', 'http://', 'https://', '//', '#', 'data:')):
                continue  # 绝对/外链不进项目图
            trel = os.path.normpath(os.path.join(os.path.dirname(rel), a))
            add_edge_if_exists(rel, trel.replace(os.sep, '/'), 'asset')
        for call in ex['calls']:
            if call in symbols or call in ('Db', 'Model', 'User', 'ApiHandler'):
                # 跨文件调用边（仅当目标在别处定义）
                if call in symbols and symbols[call]['file'] != rel:
                    key = (rel, symbols[call]['file'], 'calls')
                    if key not in edge_keys:
                        edge_keys.add(key)
                        edges.append({'from': rel, 'to': symbols[call]['file'],
                                      'kind': 'calls', 'symbol': call})

    # 孤儿检测（规划 §5.6② 仅告警不裁决）
    for name, loc in symbols.items():
        pass  # symbols 自身即定义源；孤儿针对 graph 节点引用无定义符号——此处无独立 graph 节点集，留口
    # 符号孤儿：edges 中 to 为符号文件不存在者（已在 exists 判断处理）

    graph = {'nodes': nodes, 'edges': edges}
    meta = {
        'built_at': __import__('datetime').datetime.now().isoformat(),
        'tool_version': '1.0.0',
        'root': root,
        'file_hashes': {f: file_hash(os.path.join(root, f)) for f in file_list},
        'file_mtimes': {f: _safe_mtime(os.path.join(root, f)) for f in file_list},
        'lsp_available': lsp,
        'accuracy_report': {
            'edges_total': len(edges),
            'edges_valid': len([e for e in edges if os.path.exists(
                os.path.join(root, e['to']))]) if edges else 0,
            'edges_dangling': len(dangling),
            'symbols_total': len(symbols),
            'symbols_resolved': len(symbols),
            'symbols_orphan': len(orphan_symbols),
            'static_coverage': round(include_valid / include_total, 3) if include_total else 1.0,
            'include_total': include_total,
            'include_valid': include_valid,
            'lsp_available': lsp,
        },
        'dangling_edges': dangling,
        'script_hash': file_hash(os.path.abspath(__file__)),
    }
    # 原子写（规划 §5.5）
    _atomic_write(os.path.join(out_dir, 'graph.json'), graph)
    _atomic_write(os.path.join(out_dir, 'meta.json'), meta)
    _atomic_write(os.path.join(out_dir, 'symbols.json'), symbols)
    _write_markdown(os.path.join(out_dir, 'graph.md'), graph, root)
    print(f"[GRAPH-ACCURACY] 有效边 {meta['accuracy_report']['edges_valid']} / "
          f"悬空 {meta['accuracy_report']['edges_dangling']}（已剔除）/ "
          f"include解析率 {meta['accuracy_report']['static_coverage']} / LSP: "
          f"{','.join(k for k, v in lsp.items() if v) or 'none'}")
    return graph, meta, symbols


def _atomic_write(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _write_markdown(path, graph, root):
    """graph.md 人类兜底（agent 不加载，规划 §10）。"""
    lines = ['# 项目结构图谱（人类可读兜底，agent 不加载）', '']
    for rel, n in graph['nodes'].items():
        lines.append(f"- {rel}  [classes: {', '.join(n['classes']) or '-'}]")
    lines.append('')
    lines.append('## 边')
    for e in graph['edges']:
        lines.append(f"- {e['from']} --{e['kind']}--> {e['to']}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def query(graph, meta, symbols, root, q, direction='both', depth=2):
    """规划 §9 查询接口 + 环检测。返回裁剪子图。"""
    # 解析入口
    entry = None
    if q in graph['nodes']:
        entry = q
    elif q in symbols:
        entry = symbols[q]['file']
    else:
        # 尝试按文件名匹配
        for rel in graph['nodes']:
            if rel.endswith('/' + q) or rel == q:
                entry = rel
                break
    if not entry:
        print(f"[GRAPH-QUERY] 符号索引缺失：{q}（返回空子图，未做全图扫描）")
        return {'nodes': {}, 'edges': [], 'cycle': 0}

    # 构建邻接（按 direction）+ 原边 kind 映射
    adj = {'up': {}, 'down': {}}
    edge_kind_map = {}
    for e in graph['edges']:
        adj['down'].setdefault(e['from'], []).append(e['to'])
        adj['up'].setdefault(e['to'], []).append(e['from'])
        edge_kind_map[(e['from'], e['to'])] = e['kind']

    MAX_NODES = 80  # 节点预算硬上限（规划 §9 省 token：防枢纽模块 2 跳爆炸）
    visited = set()
    subgraph_nodes = {}
    subgraph_edges = []
    cycles = [0]
    seen_cycle = set()  # 环边按 (from,to) 去重，仅保留一条（规划 §9「环只保留一条边」）

    def walk(node, d):
        if node in visited:
            return
        visited.add(node)
        if node in graph['nodes']:
            subgraph_nodes[node] = graph['nodes'][node]
        if d >= depth or len(subgraph_nodes) >= MAX_NODES:
            return
        dirs = []
        if direction in ('up', 'both'):
            dirs.append('up')
        if direction in ('down', 'both'):
            dirs.append('down')
        for dr in dirs:
            for nxt in adj[dr].get(node, []):
                if len(subgraph_nodes) >= MAX_NODES:
                    return
                # 遇已访问（环）→ 折叠标记，不展开（环边去重，仅保留一条）
                if nxt in visited:
                    cycles[0] += 1
                    # 环边引用的祖先节点可能不在子图节点集，补入避免人类兜底 graph.md 引用缺失（B-2）
                    if nxt in graph['nodes']:
                        subgraph_nodes.setdefault(nxt, graph['nodes'][nxt])
                    if (node, nxt) not in seen_cycle:
                        seen_cycle.add((node, nxt))
                        subgraph_edges.append({'from': node, 'to': nxt,
                                               'kind': 'cycle'})
                    continue
                kind = edge_kind_map.get((node, nxt)) or edge_kind_map.get(
                    (nxt, node)) or 'include'
                subgraph_edges.append({'from': node, 'to': nxt, 'kind': kind})
                walk(nxt, d + 1)

    walk(entry, 0)
    if cycles[0]:
        print(f"[GRAPH-CYCLE] 检测到 {cycles[0]} 个环（已在子图中折叠）")
    return {'nodes': subgraph_nodes, 'edges': subgraph_edges, 'cycle': cycles[0]}


def _graph_files_present(root):
    """B1：图谱三件套（graph/meta/symbols）是否齐全。任一缺失 → query 入口须重建，避免 open 崩溃。"""
    kg = os.path.join(root, '.ai-memory', 'knowledge-graph')
    return all(os.path.isfile(os.path.join(kg, f))
               for f in ('graph.json', 'meta.json', 'symbols.json'))


def need_rebuild(root):
    """规划 §6 新鲜度：比对 mtime+内容哈希。"""
    meta_path = os.path.join(root, '.ai-memory', 'knowledge-graph', 'meta.json')
    if not os.path.exists(meta_path):
        return True, 0
    try:
        with open(meta_path, encoding='utf-8') as f:
            meta = json.load(f)
    except Exception:
        return True, 0
    changed = 0
    current_rels = set()  # B3：记录当前仍存在源文件，用于检测"删除"
    mtimes = meta.get('file_mtimes', {})  # 廉价 mtime 前置过滤：mtime 未变则内容必未变
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS
                       and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith(SRC_EXTS):
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, root).replace(os.sep, '/')
                current_rels.add(rel)
                # mtime 一致（含旧版无 file_mtimes 时 mtimes={} → 不触发，回退全量 md5）
                if rel in mtimes and mtimes[rel] == _safe_mtime(p):
                    continue
                h = file_hash(p)
                if rel not in meta.get('file_hashes', {}) or meta['file_hashes'][rel] != h:
                    changed += 1
    # B3：meta 记录的文件若已不在当前树中（被删除）→ 视为变更，触发重建，避免残留悬空边
    if set(meta.get('file_hashes', {})) - current_rels:
        changed += 1
    # 脚本版本校验（规划：脚本升级应触发重建）
    if meta.get('script_hash') != file_hash(os.path.abspath(__file__)):
        changed += 1
    return changed > 0, changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.getcwd())
    ap.add_argument('--query', help='入口 file 或 symbol，多个逗号分隔合并子图')
    ap.add_argument('--direction', default='both', choices=['up', 'down', 'both'])
    ap.add_argument('--depth', type=int, default=2)
    ap.add_argument('--rebuild', action='store_true', help='强制全量重建')
    ap.add_argument('--no-rebuild', action='store_true',
                    help='跳过新鲜度检测，直接复用已缓存图谱（仅在确认图谱新鲜的连续查询时使用）')

    ap.add_argument('--selftest', action='store_true',
                    help='运行内置 E2E 自检（删文件无悬挂边 + 改文件过期判定），不改交付物')
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if args.selftest:
        import tempfile as _tf
        import shutil as _shutil
        # B-3：在副本运行，避免触碰用户原始交付物（旧版会 rename/改写原文件）
        work = _tf.mkdtemp(prefix='kg_selftest_')
        _shutil.copytree(root, work, dirs_exist_ok=True,
                         ignore=_shutil.ignore_patterns('.ai-memory', '.codebuddy', '.git'))
        kg = os.path.join(work, '.ai-memory', 'knowledge-graph')
        def load():
            return (json.load(open(os.path.join(kg, 'graph.json'), encoding='utf-8')),
                    json.load(open(os.path.join(kg, 'meta.json'), encoding='utf-8')),
                    json.load(open(os.path.join(kg, 'symbols.json'), encoding='utf-8')))
        build(work)
        g, m, s = load()
        # E2E-3: 选一个被依赖的真实源文件，删之，重建后其依赖边应不残留（悬空已剔除）
        victim = None
        for e in g['edges']:
            if e['kind'] == 'include' and os.path.exists(os.path.join(work, e['to'])):
                victim = e['to']
                break
        assert victim, 'E2E-3: 无可用 victim'
        dependents = [e['from'] for e in g['edges'] if e['to'] == victim]
        print('[E2E-3] 依赖', victim, '的文件数:', len(dependents))
        bak = os.path.join(work, victim) + '.baktest'
        os.rename(os.path.join(work, victim), bak)
        build(work)
        g2, _, _ = load()
        hanging = [e for e in g2['edges'] if e['to'] == victim]
        print('[E2E-3] 删除后悬挂边:', len(hanging), '(期望 0)')
        os.rename(bak, os.path.join(work, victim))
        # E2E-4: 改一个真实文件，need_rebuild 应报 stale
        orig = open(os.path.join(work, victim), encoding='utf-8', errors='ignore').read()
        open(os.path.join(work, victim), 'a', encoding='utf-8').write('\n// e2e touch\n')
        stale, n = need_rebuild(work)
        print('[E2E-4] 编辑后过期:', stale, '变更文件数:', n, '(期望 True/>0)')
        open(os.path.join(work, victim), 'w', encoding='utf-8').write(orig)
        _shutil.rmtree(work)
        print('[SELFTEST] 完成（副本已清理，原交付物未改动）')
        return
    kg_dir = os.path.join(root, '.ai-memory', 'knowledge-graph')

    # 冷启动 / 新鲜度（规划 §6）
    if args.rebuild:
        build(root)
        return
    if args.query:
        if args.no_rebuild and _graph_files_present(root):
            print('[GRAPH-USED-CACHE] 跳过新鲜度检测，复用已缓存图谱')
        else:
            stale, n = need_rebuild(root)
            # B1：meta.json 在但 graph.json/symbols.json 缺失（被误删/损坏）→ 即便源码未变也必须重建，
            # 否则下方直接 open(graph.json) 会抛 FileNotFoundError 崩溃。
            if stale or not _graph_files_present(root):
                print(f"[GRAPH-STALE] 图谱可能过期（{n} 个文件变更/产物缺失），正在增量重建…")
                build(root)  # v1 增量=全量重抽（四类覆盖在 build 内统一处理）
            else:
                print(f"[GRAPH-FRESH] 图谱新鲜（{n} 变更）")
        with open(os.path.join(kg_dir, 'graph.json'), encoding='utf-8') as f:
            graph = json.load(f)
        with open(os.path.join(kg_dir, 'meta.json'), encoding='utf-8') as f:
            meta = json.load(f)
        with open(os.path.join(kg_dir, 'symbols.json'), encoding='utf-8') as f:
            symbols = json.load(f)
        # P1：支持多入口（逗号分隔），合并子图——覆盖 SKILL.md Step2 P1「--query <改动文件1,改动文件2,…>」
        # 查依赖闭包的使用方式；单入口时退化为原行为。
        merged = {'nodes': {}, 'edges': [], 'cycle': 0}
        for q in args.query.split(','):
            q = q.strip()
            if not q:
                continue
            sub = query(graph, meta, symbols, root, q, args.direction, args.depth)
            merged['nodes'].update(sub['nodes'])
            merged['edges'].extend(sub['edges'])
            merged['cycle'] += sub['cycle']
        print(json.dumps(merged, ensure_ascii=False))
        return
    # 默认：全量构建
    build(root)


if __name__ == '__main__':
    main()
