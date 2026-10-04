# 编程专家 - dev-expert - 一招吃遍天下鲜

一个覆盖编程全生命周期的全栈编程助手：说需求，它自动选对工具并组合执行，你不必记任何名字。

```
                    _ooOoo_
                   88" . "88
                   (| -_- |)
                   O\  =  /O
                ____/`---'\____
              .'  \\|     |//  `.
             /  \\|||  :  |||//  \
            /  _||||| -:- |||||-  \
            |   | \\\  -  /// |   |
            | \_|  ''\---/''  |   |
            \  .-\__  `-`  ___/-. /
          ___`. .'  /--.--\  `. . __
       ."" '<  `.___\_<|>_/___.'  >'"".
      | | :  `- \`.;`\ _ /`;.`/ - ` : | |
      \  \ `-.   \_ __\ /__ _/   .-` /  /
 =====`-.____`-.___\_____/___.-`____.-'=====
                    `=---='
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          佛祖保佑       永无BUG
```

> 📌 Github 上吹得再好的技能，没有实战经验写不出有用的东西。纸上谈兵就是扯蛋……
> 🚀 **第一次用？只看这段**：直接说你的目标（如"帮我给后台加个导出按钮"），路由、组合、验证它全包了；只有"报错 / 不确定能不能做"时才需要查 FAQ。

> 📌 **TL;DR**
>
> - **是什么**：19 个子技能的全链路编程助手；说需求即自动匹配 + 自动组合，无需记名字。
> - **怎么用**：自然对话说目标，带上「目标 + 约束 + 验收」最省事；边界与报错查 FAQ。
> - **护栏**：hooks 是可选增强（备份 / lint / 安全）；红线（直拼 SQL、盲写库、跳过验证）踩了会被拦。
> - **深入**：细节在 `references/*.md`，本文件只给入口与导航。
> - **知识图谱**：`@project-knowledge-graph` 纯正则建依赖图、查询近零 token（见附录 A）；高级进阶功能，须按自身环境适配。

### ⚠️ 注意

> 本技能的目的是跨工具快速迁移：工具不好用就换，进度 / 规范 / 踩坑错误册 / 图谱都不被任何工具束缚，可随工具迁移。
> hooks 与 scripts（知识图谱）属高级进阶功能，须按自身运行时适配后生效。

## 子技能列表

> 19 个子技能一表速览。**你不需要背它们**——上表只帮你判断交付结果是否符合预期，说需求即自动匹配。

| 子技能 | 功能 | 触发关键词 |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 软件项目总控 | 通用软件项目从需求到交付的总控：边界、行为契约、架构、数据/API/集成、测试、安全、发布、回滚、监控、告警、巡检和沉淀 | 软件项目, API服务, 后端服务, 后台模块, CLI工具, 数据脚本, 自动化任务, 插件项目, 完整功能, 项目交付, 部署, 发布, 回滚, 运维, 监控, 告警, 巡检 |
| 网站项目总控 | 从需求到上线的建站项目总控：站点规划、内容SEO、前端设计、CMS/API/数据、测试安全、性能部署、验收运维 | 做网站, 建站, 企业官网, 营销页, CMS网站, 网站上线, 网站交付 |
| API设计 | 根据业务需求设计RESTful或GraphQL API接口，长任务采用 Init-Step-Poll 契约 | API设计, RESTful, GraphQL, 接口规范, AJAX防卡死, Init-Step-Poll, 长任务接口, 轮询接口 |
| Bug诊断 | 分析错误日志和异常堆栈，定位Bug根因并给出修复方案 | Bug诊断, debug, 报错, 异常堆栈 |
| Karpathy编码规范 | 提供Karpathy核心编码哲学：思考优先、简洁至上 | Karpathy编码规范, Karpathy, 编码哲学 |
| Spec驱动开发 | 编码前对齐需求规格，使用OpenSpec artifact flow | Spec驱动开发, spec, 需求对齐 |
| 代码审查 | 审查代码质量，发现Bug、安全漏洞和代码缺陷 | 代码审查, code review, 代码缺陷 |
| 代码生成 | 根据功能需求生成高质量代码，含错误处理和边界条件 | 代码生成, 生成代码, 实现功能 |
| 任务拆解与执行 | 将复杂需求拆分为原子任务，按Wave分组执行 | 任务拆解与执行, 任务分解, Wave执行 |
| 技术选型 | 根据项目需求推荐合适技术栈、框架和工具，并给出运行时基线与版本策略 | 技术选型, 技术栈, 框架选型, 运行时基线, 版本策略 |
| 文档生成 | 根据代码生成技术文档、README、API文档、部署说明和运维文档 | 文档生成, API文档, README, 部署说明, 回滚说明, 运维文档 |
| 测试用例生成 | 生成单元测试、集成测试、安全测试、性能测试和长任务测试 | 测试用例生成, 单元测试, 测试用例, 安全测试, 性能测试, 长任务测试 |
| 重构建议 | 分析代码结构，识别坏味道并提供重构方案 | 重构建议, 重构, 坏味道, 代码异味 |
| 项目记忆管理 | 捕获上下文和决策，实现跨会话项目记忆沉淀，并治理工作产物生命周期（计划 / 错误册 / 图谱 / 生成产物） | 项目记忆管理, 项目记忆, 跨会话, 产物生命周期 |
| CMS二次开发 | PHP+MySQL CMS 二次开发全链路：CMS探测/PHP版本/数据库规范/安全红线/插件开发/长任务防卡死 | CMS, 帝国CMS, WordPress, ThinkPHP, PHP8兼容, 二次开发, 插件开发, 批量任务, 导入导出, 生成静态页 |
| 前端设计 | UI/UX 与前端实现设计：设计思维、信息架构、视觉规范、品牌、Banner、图标、社媒图、响应式、可访问性、安全性、命名规范、目录规范、代码质量、ESLint基线、性能实现、浏览器验证、进度轮询 | 前端设计, UI设计, UX, 交互设计, 响应式, 设计系统, 前端安全, 命名规范, 目录规范, ESLint, 代码质量, 性能实现, 品牌设计, Banner, 图标, 社媒图, 进度条, 轮询状态 |
| MySQL数据库 | MySQL 数据建模、SQL安全、索引设计、事务边界、慢查询诊断、迁移回滚和数据安全 | MySQL, 数据库设计, SQL, 索引, 事务, 慢查询, EXPLAIN, DDL, 迁移, 表结构, SQL优化 |
| 性能基准测试 | 量化性能验证：识别触发面、测量耗时/内存/吞吐量、生成瓶颈报告、优化前后A/B对比 | 性能测试, benchmark, 基准测试, 耗时分析, 内存分析, 吞吐量, QPS, 瓶颈分析, 性能对比 |
| 项目知识图谱 | 为项目自动构建代码结构依赖图谱（节点+依赖边），跨模块改动/重构/审查时查依赖闭包与影响面；纯 agent 受众，不生成 mermaid 可视化 | 依赖图, 模块关系, 谁依赖, 影响面, 代码结构图谱, 画依赖图, 依赖分析, 改这个会影响哪些文件 |

## 使用方法

### 3 分钟上手

| 你想做什么 | 推荐说法 | 会进入 |
| ------------------ | ------------------------------------------------- | ------------------------------------ |
| 写一个功能 | "帮我实现登录接口，要求有参数校验和测试" | 代码生成 + 测试用例生成 |
| 修一个报错 | "这个报错帮我定位原因并给修复方案" | Bug诊断 |
| 检查代码有没有问题 | "审查这个文件，重点看安全和性能" | 代码审查 |
| 做 CMS/PHP 二开 | "这是 WordPress/帝国CMS 项目，帮我加一个后台功能" | CMS二次开发 |
| 设计接口 | "设计一个订单导出接口，数据量大，需要进度条" | API设计 + Init-Step-Poll |
| 换电脑继续上次任务 | "继续上次任务，先恢复 handoff" | 项目记忆管理 |
| 顺带做两件事 | "实现导出接口，顺带生成接口文档" | 代码生成 + 文档生成 |
| 不知道功能叫啥 | "帮我看看这段代码安不安全" | 代码审查（描述目标即可，不必记名字） |

### 需求怎么说最省事

万能公式：**目标 + 约束 + 验收**。越齐，追问越少。

- ❌ 太模糊：`帮我把系统优化一下` → 会触发 Wayfinder 探索，先和你对齐再动手（不是错，但慢）。
- ✅ 直接命中：`用户列表接口响应超过 2s，帮我定位慢查询并加索引，目标降到 200ms 内` → 命中 `mysql-database` + `performance-benchmark`。
- ✅ 带约束：`给后台加一个导出用户的功能：范围=按筛选条件、格式=CSV、要鉴权+限频、能正确导出 1 万行且带表头`。
- ✅ 顺带式：`实现登录接口，并生成单元测试`；`定位这个报错，顺带看看附近代码有没有安全隐患`。
- ✅ 纠正：`刚才那个修复不对，第 12 行的判空应该用 if x is None 而不是 if not x` → 重做并复跑验证。

> 关键：**说目标比背名字更稳**。不确定叫啥就直接描述；命中不了会问你一句，不会偷偷用错技能。

### ⚠️ 上手前先扫一眼红线

- **不覆盖的领域**：用户调研、工时排期、容器深度编排、IDE 配置、缺陷跟踪流程、安全深度扫描（只做边界说明）。
- **仅覆盖判据 / 载体 / 度量口径层（不含组织决策）**：`technical-strategy`、`tech-influence`、`engineering-metrics`。
- **执行禁区**：直拼 SQL、Shell 写中文/UTF-8 文件、跨模块扩散修改、硬编码密钥、跳过验证直接交付、为让验收通过而改测试 / 放宽断言、安全/数据类失败重试、凭猜测补业务规则、快速通道执行数据库写入、跨模块(≥2)/批量替换(>10处) 走快速通道。
- **关键限制**：流程按任务档位剪裁（**轻量 / 常规 / 复杂 / 大项目**，执行集见 `references/routing.md`「档位 → 最小执行集」）；单次最多加载 3 个协同 reference（**Step 强制加载集不计**）；子 Agent 禁止写/改代码（只做检索收集）；代码审查是**只读**的、不自动改写实现；Laravel / Java / JS 等专项 reference 不支持 `@` 显式调用（用关键词触发）；涉库写入 / 权限 / 生产配置须先给方案与回滚路径。

> ⚠️ 红线不是建议：直拼 SQL / 盲写库 / 跳过验证直接交付，踩了会被安全闸门拦截、交付判无效。

### 文档阅读顺序

| 场景 | 先看 | 再看 |
| -------------------------- | --------------------------------------------------- | ------------------------------------- |
| 只想知道怎么用 | 本文件「3 分钟上手」与「子技能列表」 | `FAQ.md` |
| 不知道该用哪个技能 | 本文件「子技能列表」 | `references/routing.md` 领域路由表 / 优先级矩阵 |
| 遇到报错、卡住、看不懂提示 | `FAQ.md` | 对应 `references/*.md` 的失败回退机制 |
| 长任务执行 / 续做 / 可靠交付 | `FAQ.md` 第九节 | `references/task-decomposition-and-execution.md` |
| 要改技能执行规则 | `SKILL.md`（薄入口 + 强制加载表） | 对应 `references/*.md` |
| 想先知道哪些不能做 / 红线 | `FAQ.md`「能力边界速览」/ 二、执行禁区 / 六、边界外 | `references/execution-safety.md` 安全闸门 / 澄清策略分级 |

### 组合与进阶

- **组合是自动的**：说清完整目标（如"实现导出功能并出接口文档"）即自动串联（代码生成 + 文档生成），不必手动点名先后。
- **想精确控制时才显式表达**：① 顺带式点名；② 多个 `@`（"`@code-review` 先审，`@refactoring` 再重构"）——只跳过路由匹配，不影响协同加载。
- **典型顺序**：审查类（代码审查 / Bug诊断）只读，先出报告、你确认后再走重构 / 生成；性能类先跑基线再重构，禁止无基线声称提升。
- **完整协同顺序（19 条）与优先级矩阵**：见 `references/routing.md`「协同顺序规则」（本文件不再重复清单）。

## Hooks 自动守卫（可选，高级进阶；须按自身运行时适配）

> **非开箱即用**：须按自身运行时部署 / 接入后才生效。共 26 个可选护栏钩子（PreToolUse 7 + PostToolUse 18 + PreCompact 1），跨 IDE 用**工具名并集匹配（matcher）**，接入后自动匹配。

覆盖机械兜底项：备份、lint、PHP8 兼容、安全 / 脱敏、UTF-8、调试残留、`SELECT *`、压缩快照、规划拦截、受保护目录写前拦截、写入前综合检查、数据外发拦截、踩坑召回 / 查重、图谱影响面、日迹归档、步骤号引用一致性。

### 设计要点（每条可在 `hooks/*.py` 中检索到依据）

| # | 设计要点 | 依据 |
| - | - | - |
| 1 | **写前阻断是最强的送达通道**——PostToolUse 裸 stdout 不回传 Agent（其 `hookSpecificOutput.additionalContext` JSON 可送达），只有 PreToolUse `exit 2` 能回传**拒绝理由**；故「必须拒绝」的检查走写前 | `hooks/precheck_on_write.py:3-7`、`rule_ref_guard.py:56-62` |
| 2 | **组合模式压误报**——安全项要求「危险函数 **且** 用户输入源」同现才命中；`replace_in_file` 只审 `new_str` 片段 | `precheck_on_write.py:47-50`、`:19-23` |
| 3 | **失败一律放行**——任何异常 / 依赖缺失 / 解释器不可用 → 静默 `exit 0`，绝不误拦 | 各脚本 `except → return 0` 早退 |
| 4 | **依赖探测链，不写死路径**——PHP 按 `PHP_BIN` → 多版本环境变量 → 三平台候选目录 × 版本降序解析；Java 走 `javac` 且只认白名单语法错 | `lint_on_write.py:20-39`、`:6-9` |
| 5 | **防杀软自伤**——危险函数名 / 敏感词一律字符串拼接构造，并防「钩子被再次写入时自己拦自己」 | `precheck_on_write.py:31-32`、`secret_scan.py:13-15` |
| 6 | **一套配置跨 IDE**——matcher 工具名并集（`write_to_file\|replace_in_file\|Write\|Edit`）；五路证据探测在用工具；幂等只追加不删除；对「技能安装目录 / 模板自身」两重拒写 | `scripts/hooks.json:2`、`scripts/init_deploy.py` |

### 能力矩阵

| 维度 | 覆盖规模 | 钩子 |
| - | - | - |
| 写前阻断 | 4 类内容级检查（PHP 语法 / 调试残留 / 安全组合 / 语言规范），命中 `exit 2` 拒写并回传理由 | `precheck_on_write` |
| 回滚网 | 改写前自动 `.bak`，保留最近 10 版（`.bak` + `.bak.1`…`.bak.9`）；内容一致跳过、新文件不备份、8 类目录豁免、23 种扩展名生效 | `backup_on_write` |
| 边界守卫 | 4 个受保护目录（`uploads` / `backup` / `vendor` / `node_modules`）拒写；核心目录改动前要求存在进行中的 `*_plan.md`（默认 7 核心目录 / 15 排除目录 / 9 扩展名，可 env 覆盖） | `guard_dirs`、`plan_guard` |
| 语法自检 | 3 语言：PHP `php -l` / Java `javac`（白名单过滤）/ Python `py_compile` | `lint_on_write` |
| 兼容扫描 | PHP 8.x 3 类（短标签 / 裸数组键 / `each`·`create_function`·`get_magic_quotes_gpc`，跳过全大写常量）；Java 10 个版本特性按目标版本判定，探测不到即静默 | `php8_compat`、`java_compat` |
| 安全扫描 | PHP 5 规则 + Java 6 规则（原生反序列化 / 命令执行 / SQL 拼接 / XXE / 弱哈希加密 / 堆栈外泄） | `security_scan` |
| 数据外发拦截 | 写前检测「外发调用 **且** 敏感来源」组合，覆盖 PHP / Python / JS·TS / Java / Go / Shell | `egress_scan` |
| SQL 注入 | 7 风险模式 × 13 种扩展名 × 5 语言；含 MySQL 高危关键字（`LOAD DATA` / `INTO OUTFILE` / `GRANT`）；4 类安全模式跳过 | `sql_injection_check` |
| CMS / 框架 | 37 条规则 = 18 条 CMS/框架 SQL 注入 + 7 条框架特有 + 12 条通用风险，覆盖 17 个生态（帝国 / 织梦 / Discuz / WordPress / PHPCMS / Drupal / Joomla / ThinkPHP / CI / Laravel / Yii / Symfony / Typecho / ZBlog / Emlog / PDO / mysqli） | `cms_risk_check` |
| 脱敏 | 硬编码明文凭证（12 类凭证名变体）+ 日志 / 文件写入含敏感变量 | `secret_scan` |
| 调试残留 | 4 语言族（PHP `var_dump`·`print_r`·`die`；JS·TS `console.log`；Java·Kotlin `System.out.print*`·`printStackTrace`；Laravel·Symfony `dd`·`dump`），17 种扩展名，跳过 `tests/` | `debug_residue` |
| 依赖漏洞 | 7 生态（npm / yarn / pnpm · pip · composer · Go · Maven / Gradle · Ruby）依赖文件变更即提示对应 `audit` 命令 | `dep_scan` |
| 学习闭环 | 捕获错误信号 → 错误册 → ≥3 次且 ≥2 任务且 30 天窗口才建议升规则；非阻塞、不自动写文件 | `capture_learning`、`errors_recall_guard`、`errors_dup_guard`；`recurrence_promote`（手动） |
| 图谱兜底 | 写代码后附上游 2 跳依赖摘要（≤5 文件 / 15s 超时）；三件套齐全才查、`--no-rebuild` 绝不重建、无上游则静默 | `graph_impact` |
| 上下文与卫生 | 压缩前落检查点快照；超期日迹归档（只移不删）；技能文档改动后自动跑步骤号一致性校验；`select_star`、`utf8_check` | `handoff_snapshot`、`memory_prune`、`rule_ref_guard` |

### 三个 hooks 文件的关系（源 / 增量草案 / 安装产物）

三者都在 **`scripts/`**（与唯一消费者 `scripts/init_deploy.py` 同目录）；`hooks/` 只放被注册的运行时钩子脚本。

| 文件 | 类别 | 作用 |
| -------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------ |
| `hooks.json` | 主模板（源，手写） | 26 个守卫钩子完整定义；占位符 `{{PYTHON_BIN}}` / `{{HOOKS_DIR}}` 由运行时或部署器替换；**不含** `UserPromptSubmit` 段 |
| `hooks.capture-draft.json` | 增量草案（源，可选） | 同一条 `capture_learning.py` + 额外一条 `UserPromptSubmit`（`--mode correction`，抓你的纠错句式）。因非所有 IDE 支持该事件名，**单列 opt-in** |
| `hooks.installed.json` | 安装产物（自动生成，勿手改） | 占位符已替换为真实路径的可加载配置；每次 `--apply` 重写；`.gitignore` 已排除 |

### 一键初始化部署

**前置：Python ≥3.8**（本步骤与 hooks、图谱、步骤号校验的唯一运行时依赖）：

- Agent 先**实际执行**探测 `py -3` → `python` → `python3`（用 `-c "import sys;print(sys.executable)"`，以识别 Windows Store 假别名），命中即作为 `PYTHON_BIN`。
- 未检测到 → **先告知、经你同意后自动安装**（不静默）：Windows `winget install -e --id Python.Python.3.12 --scope user` / macOS `brew install python@3.12` / Debian·Ubuntu `sudo apt-get install -y python3` / RHEL·Fedora `sudo dnf install -y python3` / Alpine `sudo apk add python3`；装完自动复检。
- 安装失败或你不装 → 跳过 hooks 部署与图谱，**技能核心不受影响**（对应检查回退正文手动执行）。

```bash
python scripts/init_deploy.py                          # 第一步：只探测出计划（默认 dry-run，不写文件）
python scripts/init_deploy.py --apply                  # 第二步：落地（写前 .bak；只追加不删除；同名冲突默认跳过）
python scripts/init_deploy.py --scope both --apply     # 作用域 project（默认）/ user（⚠️ 影响所有项目）/ both
python scripts/init_deploy.py --tools codebuddy,trae --apply
python scripts/init_deploy.py --root D:/proj --apply --copy-to-project
python scripts/init_deploy.py --json                   # 机器可读
```

**探测依据（五路证据任一命中即视为"在用"）**：`exe`（常见安装位置可执行文件）｜`cmd`（PATH 命令名）｜`data`（应用数据目录）｜`user_cfg`（用户级配置落点存在）｜`proj_cfg`（项目级配置落点存在）。内置工具：CodeBuddy CN、Trae（Trae CN）、Cursor、Claude Code、Windsurf；跨平台、不写死任何机器路径（全部经 `%VAR%` / `~` 展开）；工具未探测到 → 不写。

**它会做什么**：① 探测在用工具 + 配置落点 + 按 `hooks.json` 引用逐个校验 `*.py`（缺项直接报错且不写盘）；② 按 `--scope` 生成「工具 × 作用域」落点清单并幂等合并写入（单目标失败不影响其他）；③ 逐目标回读校验 JSON 合法 + 每个 command 指向的脚本存在。

**安全保证**：默认 dry-run；`--apply` 才写；写前 `.bak`；只追加不删除；同名冲突默认跳过（`--allow-overwrite` 才替换）；`--scope user|both` 会提示「影响该用户所有项目」；项目根疑似技能安装目录、或目标配置与技能模板同文件时自动拒绝写入。未探测到任何工具时仍生成 `hooks.installed.json`，按方式 B 手动接入即可。

**启用方式（任选其一）**：

- **方式 A（占位符替换，适用于支持变量替换的 IDE）**：把 `hooks.json` 接入运行时，设环境变量 `PYTHON_BIN`（解释器路径）与 `HOOKS_DIR`（hook 脚本目录，可指技能自带 `hooks/` 或你项目 `.codebuddy/hooks/`），加载时替换占位符。
- **方式 B（安装器预处理，推荐跨平台）**：`python hooks/install_hooks.py`（可加 `--python-bin` / `--hooks-dir`，或设同名环境变量）生成 `hooks.installed.json`，直接接入；`--in-place` 原地覆盖（自动备份 `.bak`）。换机 / 换项目重跑即可。

> 平台落点声明集中在 `scripts/platforms.json`（探测器唯一数据源，缺失或非法时**拒绝启动**，退出码 2，不静默降级为空表）：记录各工具的探测路径 / hooks 配置落点 / skill 加载目录与命名约定 / 平台注册表，逐字段标可信度（`measured` / `documented` / `candidate` / `unknown`）。**它仅作声明，不自动安装 skill、不写任何平台注册表**。可用 `--platforms <路径>` 指定外部声明。

> hooks 是护栏不是验证替代：动态 / 业务正确性（真实运行、端到端）仍须 Agent 显式产出证据；被拦即视为该防线未过，禁止绕过；运行时无 hooks 集成时回退正文手动执行。故障排查见 `FAQ.md` 十五。

### 适配平台（多 IDE）

这是**匹配层**能力，不等于开箱即用：须先按自身运行时完成接入与环境适配，之后只要工具名落在下表某个家族里即被自动匹配。工具名不同时在 matcher 用 `|` 追加一行即可，无需改脚本。

| 平台 | 工具名家族 | matcher | 落点 / 说明 |
| ----------------------- | ---------------------------------------------- | --------- | ---------------------------------------------------------------------- |
| **CodeBuddy CN** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | `~/.codebuddy/settings.json` 或 `~/.codebuddycn/settings.json`（实测均含 hooks 键） |
| **Trae / Trae CN** | `Write` / `Edit` | ✅ 已覆盖 | 实测 `~/.trae-cn/hooks.json`；`~/.trae/hooks.json` 作候选 |
| **Cursor** | `Write` / `Edit` | ✅ 已覆盖 | 代码 / 历史已确认 |
| **Qoder CN** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | 实测 `~/.qoder-cn/settings.json`；官方文档 `~/.lingma/settings.json` 作候选 |
| **WorkBuddy** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | 实测 `~/.workbuddy/settings.json`（含 hooks 键） |
| **Claude Code** | `Write` / `Edit` / `Bash` / `UserPromptSubmit` | ✅ 已覆盖 | 事件最全；`UserPromptSubmit` 可选 |
| **Codex / Gemini CLI / OpenClaw** | `Bash` / 命令类 | ✅ 已覆盖 | 命令类家族 |
| **Cline / Roo Code** | `write_to_file` / `replace_in_file` | ⚠️ 仅工具名同族 | 寄生 VS Code；实测无文件式 hooks 落点（配置在扩展 `globalState.json`），需手工接入或不适用 |
| **Windsurf** | `write_file` / `edit_file` | ⚠️ 需追加 | 在 matcher 补 `write_file \| edit_file` |
| **Zed / Continue** | 视配置 / 扩展 | ⚠️ 待确认 | 确认工具名后追加 |
| **Aider** | CLI 自有机制 | ❌ 不适用 | 走自带 hook / 包装层，不在 matcher 范围 |

**追加未列出的平台**：编辑 `hooks.json` 每个 matcher 字符串，用 `|` 并入新工具名（例如加上 `MultiEdit`、`save_file`）。**额外名称不匹配时无害**，可放心并集；改完重跑安装器即可。

**事件键裁剪**：若运行时因未知事件名导致整份配置加载失败，用 `python scripts/init_deploy.py --events PreToolUse,PostToolUse --apply` 只保留受支持事件；**默认全量不裁剪**（本技能模板只注册 `PreToolUse` / `PostToolUse` / `PreCompact`；其余平台事件清单未逐一查证）。

> ⚠️ **长任务 / 捕获 hook 要"自动执行 + 自动测试"须开放运行时权限**：`capture_learning.py` 与长任务闭环要自主跑通「执行命令 → 跑测试（`php -l` / `phpunit` / `node --check`）→ 落记录」，依赖运行时授予 `Bash` / `execute_command` 的**免确认执行权限**。两层开放：① 技能侧 `SKILL.md` 的 `allowed-tools` 已声明；② 运行侧须允许这些工具 auto-approve。未开放时须退化为「每步请求确认」模式，不得假设可无人值守自动执行。

## 协同技能

19 个子技能通过各自文末的 `## 关联 reference` 章节相互引用（专项 reference 的协同由 `references/routing.md`「专项 reference 映射」收口）。常见链路的形状（非穷举，**完整 19 条以 `references/routing.md`「协同顺序规则」为唯一真源**）：

- 交付型：Spec驱动开发 → 任务拆解与执行 → 代码生成 → 代码审查 → 测试用例生成 → 文档生成 → 项目记忆管理
- 治理型：Bug诊断 / 重构建议 → 代码审查 → 项目记忆管理
- 专项型：CMS二次开发 / MySQL / Laravel / Java / 性能基准测试 → 按需协同代码生成、代码审查、测试用例生成
- 本技能包为独立套件，暂无可联动的其他职业技能包；需外部数据或服务时用主 Agent 可用的检索工具。

## 文件结构

- `SKILL.md` - 技能运行时指令（**薄入口**：六步骨架 Step 0–6 + 门禁索引 + 强制加载表；细则在 `references/`，按步强制加载）
- `README.md` - 本文件，用户入口文档
- `FAQ.md` - 常见问题、执行禁区、验证失败与边界外请求答疑
- `hooks/` - 钩子脚本目录（高级功能，须按自身 IDE 适配）：26 个守卫钩子（备份/lint/计划质量守卫/命令卫生/测量口径提示/PHP8 与 Java 版本兼容/安全/数据外发拦截/脱敏/UTF-8/调试残留/`SELECT *`/依赖扫描/SQL注入/CMS风险/学习捕获/压缩快照/规划拦截/受保护目录拦截/写入前综合检查/踩坑召回/踩坑查重/图谱影响面/日迹归档/步骤号引用一致性）+ `install_hooks.py` 安装器 + `step_ref_check.py` + `recurrence_promote.py`
- `scripts/init_deploy.py` - 初始化部署器（工具，非钩子；默认 dry-run）
- `scripts/build_graph.py` - 知识图谱构建/查询（纯正则、零 LLM token）：`--root` 全量 / `--query <file|symbol> [--direction up|down|both] [--depth N]` / `--rebuild` / `--incremental` / `--selftest`；产物 `{PROJECT_ROOT}/.ai-memory/knowledge-graph/{graph,meta,symbols}.json`
- `scripts/hooks.json` - hooks 主模板（源，手写维护）
- `scripts/hooks.installed.json` - hooks 安装产物（自动生成，勿手改；首次部署前不存在，不入版本库与发布包）
- `scripts/platforms.json` - 平台落点声明（单一事实源；缺失即 fail-closed）
- `scripts/hooks.capture-draft.json` - 捕获 hook 增量草案（可选 opt-in）
- `references/` - **共 46 个 md**：19 个子技能详细模板 + 25 个专项 reference + 1 个路由层 reference（`routing.md`）+ 1 个推理与工具行为协议（`agent-reasoning-patterns.md`）（不计入子技能，其中 11 个为工程纪律层专项）
- `references/task-decomposition-and-execution.md` - 任务拆解与执行（五要素结构 / Wave 链式执行 / Task Summary / checkpoint / 证据归档 / 子 Agent 委派纪律 / 无断点执行协议）
- `references/routing.md` - 路由层：子技能索引 / 领域路由表 / 优先级矩阵 / 互斥 / 协同顺序（19 条）/ 专项映射 / 意图三分法 / Wayfinder / 加载经济与执行集（**档位 → 最小执行集**单一定义源）
- `references/agent-reasoning-patterns.md` - 推理与工具行为协议（按需加载）：16 条模式 + 思维链五段式骨架 + Method 四步硬序 + 推理侧重校准 + 思维链强度分档（档位名：轻量 / 常规 / 复杂 / 大项目，判据见 `routing.md`）+ 高阶思维模式（含防套路化 / 链内纠偏留痕）+ 验证自检（元验证）
- `references/delivery-assurance.md` - 交付保障：执行率自检（24 条，含覆盖完整性收口 / 真人功能验证 / 迁移完整性 / 防作弊 / 信心门控 / 推理外化 / 报告口径 / 产物与探针卫生）/ 信心门控 / 抗合理化 / 收尾报告 / 未验证项披露 / 确认超时 / Graceful Abort
- `references/execution-safety.md` - 执行安全：规划门禁（三池 + 规划自审 + 方案成形自检）/ 审计修复分离 / 批量修改防线 / 写码前确认与诊断先行 / 失败计数与升级 / 质量与安全清单 / 防 AI 通病五戒 / 架构一致性铁律 / 覆盖完整性枚举 / 配对契约核验 / 真人功能验证硬约束 / 保护型守卫作用范围 / 动作决策轴 / 边界判定正反例
- `references/mysql-database.md` - MySQL 专项（含「SQL 动态构建验证铁律」）
- `references/error-ledger.md` - 踩坑错误册（索引 + 单条模板 + 触发定位读取 + 新坑即录 + 归档）
- `references/style-alignment.md` - 风格对齐（二开前强制取样原项目、产出风格基线逐行对齐）
- `references/architecture-decision.md` - 架构决策（候选 + trade-off + 反选论证 + 撤销条件）
- `references/cms-development.md` - CMS 二次开发专项
- `references/frontend-design.md` - 前端设计专项
- `references/design-audit.md` - UI 改造场景审计专项
- `references/design-critique.md` - 设计评审与认知负荷专项
- `references/api-design.md` - API 设计专项
- `references/software-project.md` - 软件项目总控专项
- `references/website-project.md` - 网站项目总控专项
- `references/spec-driven-development.md` - Spec 驱动开发专项
- `references/code-generation.md` / `code-review.md` / `refactoring.md` / `test-generation.md` / `bug-diagnosis.md` / `doc-generation.md` / `tech-selection.md` / `performance-benchmark.md` / `karpathy-coding-guidelines.md` / `project-memory-management.md` / `project-knowledge-graph.md` - 各子技能主模板
- `references/laravel-development.md` / `laravel-testing.md` / `java-development.md` / `java-testing.md` / `javascript-development.md` - 框架专项（不计入子技能）
- `references/domain-driven-design.md` / `distributed-systems.md` - 领域建模与分布式专项
- `references/root-cause-debugging.md` / `dev-navigation.md` / `incident-review.md` / `threat-modeling.md` / `production-readiness.md` / `ai-coding-governance.md` / `code-readability-for-agents.md` / `llm-application-security.md` / `technical-strategy.md` / `tech-influence.md` / `engineering-metrics.md` - 工程纪律层专项

## 维护

- **体量**：单个 reference 建议 ≤400 行；`SKILL.md` ≤8000 字符（平台硬线，超出即静默截断）。
- **自检命令**：`python hooks/step_ref_check.py`（步骤号引用一致性，退出码 0=匹配）；`python scripts/init_deploy.py`（脚本完整性，dry-run）。
- **本仓专用门禁（不属技能包、不随分发）**：`tests/_de_gate_structure.py` / `_de_gate_hooks.py` / `_de_egress_check.py` / `_de_cot_ref_check.py` / `_de_skill_audit.py` / `_de_flow_audit.py`。换机或单独取用技能后这些路径不存在属预期，技能本体不依赖它们。
- **质量自评基线（9 维，本仓自定判据）**：当前 93/100；扣分项＝部分 reference 未声明异常路径、`allowed-tools` 字段有效性待对照规范、`version` / `author` 未收进 `metadata`。分数仅用于本仓纵向对比（单变量迭代：涨分保留、平/跌回滚），不可与其他项目横向比较。

## 附录 A：知识图谱 token 消耗对比

估算量级（非精确计费）；基准：332 文件 / ~5 万行 CMS 项目，图含 2890 有效依赖边，节点硬上限 `MAX_NODES=80`。

| 维度 | 常规 LLM 理解（无图谱） | 知识图谱方式 |
| --------------- | -------------------------------------------------- | ---------------------------------------------- |
| 构建 / 索引成本 | 无（每次现读源码） | 0 token（纯正则本地抽取，不进 LLM 上下文） |
| 单次依赖查询 | 6k–60k token（把 5–50 个源文件喂进上下文） | 1k–3k token（返回子图 JSON，≤80 节点） |
| 10 次任务累积 | 60k–600k token | 10k–30k token |
| 跨会话复用 | 每次重读，不留存 | 图谱缓存复用，query 恒定 ~2k |
| 上下文污染 | 大（源码占满窗口） | 小（仅依赖拓扑，不含实现细节） |

**为何能省**：把「代码 → 依赖」的抽取放在 LLM 之外（纯正则静态抽取，LSP 仅探测可用性、不参与抽取），LLM 只消费精简后的依赖拓扑 JSON。构建阶段 token≈0、查询阶段不重读源码；单次节省约 70%–95%，跨会话累积更显著。详见 `references/project-knowledge-graph.md`。
