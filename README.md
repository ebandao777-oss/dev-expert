# 编程专家 - dev-expert

面向软件工程师和开发团队的编程全生命周期助手。覆盖从软件项目总控、网站项目总控、需求分析、前端设计、MySQL数据库、代码生成、Bug诊断到重构、测试、文档、上线交付和运维监控的全链路，通过19个子技能提供专业化支持。特别强化PHP+MySQL CMS二次开发场景，提供CMS自动探测、PHP版本选型、数据库规范、安全红线、AJAX渐进式防卡死等专项指引；Laravel/PHP、Java/Spring 框架能力以专项参考文档方式按需加载，不新增子技能入口。
```
                    _ooOoo_
                   o8888888o
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
### 为什么保留渐进式路由（而非一步直达）

你可能会问：既然"说需求即自动匹配"，为什么 SKILL.md 还要保留 `@显式调用 → 关键词 → 领域路由表 → 优先级矩阵 → 意图三分法` 这套多层、逐级收窄的**渐进式路由**，而不是直接让模型凭一句话判断进哪个子技能就执行？

因为渐进式路由**不是单纯的"分类器"，而是六步闭环工作流（Step 0–6）的入口分发轨道**——它的每一层输出都挂着后续的一道门。抛离路由等于拆掉轨道：模型仍会"做事"，但流程会从中间断裂，丢失可验证、可恢复、可审计的保证。

| 路由层 | 它挂接的后续步骤（不抛离的原因） |
| --- | --- |
| `@显式` / 关键词 / 领域路由表 | 命中结果决定加载哪个 `reference` 主模板，模板里的澄清门控、验证证据、SELF-AUDIT 清单才有挂载点 |
| 领域路由表的「路由边界」列 | 提前识别"不在本技能范围"的请求（用户调研 / 排期 / 容器编排 / 安全深度扫描），只做边界说明不硬覆盖 |
| 优先级矩阵（40+ 行「X+Y」场景） | 决定**组合协同顺序**（先审查后重构、先基线后对比、CMS 规范优先于代码生成），无此则组合失据 |
| 意图三分法（信息查询 / 简单任务 / 复杂任务） | 决定走快速通道还是先方案确认——**安全闸门的触发点就在这里**，抛离会跳过生产配置 / DB 写入的事先确认 |

如果完全抛离、改为一步直达，会同时丢掉四道关：Step 1.5 澄清门控（模糊形容词直接动手，做完才发现理解不一致）、Step 2 安全闸门（DB / 生产配置未确认即执行）、Step 4 验证证据 + Step 5 SELF-AUDIT（无证据交付）、长任务 handoff / Wave 的主模板锚点（上下文压缩后无法无损续做）。

> 一句话：**渐进式路由保的是"工作流不断裂"**——可验证、可恢复、可审计的闭环都挂在它上面。你描述目标时感觉不到它，是因为它已经在后台把每道门按顺序挂好了。

**那为什么 SKILL.md 显得很大？** 不是路由本身臃肿，而是同一份文件把"分发轨道 + 闭环步骤 + 护栏边界"三件必须共存的东西压在了一起：

- **闭环步骤是硬骨架**：Step 0 记忆加载 → Step 1 意图路由 → Step 1.5 澄清门控 → Step 2 规划门禁 → Step 3 执行（7 防线）→ Step 4 验证证据 → Step 5 交付 + SELF-AUDIT → Step 6 复盘沉淀。每一步都不能省，否则闭环断一节。
- **路由是轨道、护栏是闸**：路由表 / 领域路由表 / 优先级矩阵 / 意图三分法负责"分发"，安全闸门、失败重试基线、对话流异常边界、子 Agent 边界、长任务可靠性负责"兜底"——它们必须和步骤写在同一份运行时指令里，模型加载 SKILL.md 时才一次拿到全部门控。
- **为什么没拆进 references**：references/ 下 26 个文件是"各子技能的详细模板"，而 SKILL.md 是"总控流程 + 跨步骤门控"。门控若拆出去，模型要先跳读多个文件才知道哪步该停，反而增加断裂风险。所以 SKILL.md 故意"大而全"，references 才"专而深"。

> 简言之：**大是为了不断裂**——闭环骨架 + 分发轨道 + 兜底护栏都必须在同一次加载里齐备，拆散反而会让模型在某步"忘了该不该停下"。真正会被按需懒加载的细节，都在 references/ 里，不用一次读完。

## 子技能列表

| 子技能           | 功能                                                                                                                                                                               | 触发关键词                                                                                                                                                   |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 软件项目总控     | 通用软件项目从需求到交付的总控：边界、行为契约、架构、数据/API/集成、测试、安全、发布、回滚、监控、告警、巡检和沉淀                                                                | 软件项目, API服务, 后端服务, 后台模块, CLI工具, 数据脚本, 自动化任务, 插件项目, 完整功能, 项目交付, 部署, 发布, 回滚, 运维, 监控, 告警, 巡检                 |
| 网站项目总控     | 从需求到上线的建站项目总控：站点规划、内容SEO、前端设计、CMS/API/数据、测试安全、性能部署、验收运维                                                                                | 做网站, 建站, 企业官网, 营销页, CMS网站, 网站上线, 网站交付                                                                                                  |
| API设计          | 根据业务需求设计RESTful或GraphQL API接口，长任务采用 Init-Step-Poll 契约                                                                                                           | API设计, RESTful, GraphQL, 接口规范, AJAX防卡死, Init-Step-Poll, 长任务接口, 轮询接口                                                                        |
| Bug诊断          | 分析错误日志和异常堆栈，定位Bug根因并给出修复方案                                                                                                                                  | Bug诊断, debug, 报错, 异常堆栈                                                                                                                               |
| Karpathy编码规范 | 提供Karpathy核心编码哲学：思考优先、简洁至上                                                                                                                                       | Karpathy编码规范, Karpathy, 编码哲学                                                                                                                         |
| Spec驱动开发     | 编码前对齐需求规格，使用OpenSpec artifact flow                                                                                                                                     | Spec驱动开发, spec, 需求对齐                                                                                                                                 |
| 代码审查         | 审查代码质量，发现Bug、安全漏洞和代码缺陷                                                                                                                                          | 代码审查, code review, 代码缺陷                                                                                                                              |
| 代码生成         | 根据功能需求生成高质量代码，含错误处理和边界条件                                                                                                                                   | 代码生成, 生成代码, 实现功能                                                                                                                                 |
| 任务拆解与执行   | 将复杂需求拆分为原子任务，按Wave分组执行                                                                                                                                           | 任务拆解与执行, 任务分解, Wave执行                                                                                                                           |
| 技术选型         | 根据项目需求推荐合适技术栈、框架和工具                                                                                                                                             | 技术选型, 技术栈, 框架选型                                                                                                                                   |
| 文档生成         | 根据代码生成技术文档、README、API文档、部署说明和运维文档                                                                                                                          | 文档生成, API文档, README, 部署说明, 回滚说明, 运维文档                                                                                                      |
| 测试用例生成     | 生成单元测试、集成测试、安全测试、性能测试和长任务测试                                                                                                                             | 测试用例生成, 单元测试, 测试用例, 安全测试, 性能测试, 长任务测试                                                                                             |
| 重构建议         | 分析代码结构，识别坏味道并提供重构方案                                                                                                                                             | 重构建议, 重构, 坏味道, 代码异味                                                                                                                             |
| 项目记忆管理     | 捕获上下文和决策，实现跨会话项目记忆沉淀                                                                                                                                           | 项目记忆管理, 项目记忆, 跨会话                                                                                                                               |
| CMS二次开发      | PHP+MySQL CMS 二次开发全链路：CMS探测/PHP版本/数据库规范/安全红线/插件开发/长任务防卡死                                                                                            | CMS, 帝国CMS, WordPress, ThinkPHP, PHP8兼容, 二次开发, 插件开发, 批量任务, 导入导出, 生成静态页                                                              |
| 前端设计         | UI/UX 与前端实现设计：设计思维、信息架构、视觉规范、品牌、Banner、图标、社媒图、响应式、可访问性、安全性、命名规范、目录规范、代码质量、ESLint基线、性能实现、浏览器验证、进度轮询 | 前端设计, UI设计, UX, 交互设计, 响应式, 设计系统, 前端安全, 命名规范, 目录规范, ESLint, 代码质量, 性能实现, 品牌设计, Banner, 图标, 社媒图, 进度条, 轮询状态 |
| MySQL数据库      | MySQL 数据建模、SQL安全、索引设计、事务边界、慢查询诊断、迁移回滚和数据安全                                                                                                        | MySQL, 数据库设计, SQL, 索引, 事务, 慢查询, EXPLAIN, DDL, 迁移, 表结构, SQL优化                                                                              |
| 性能基准测试     | 量化性能验证：识别触发面、测量耗时/内存/吞吐量、生成瓶颈报告、优化前后A/B对比                                                                                                      | 性能测试, benchmark, 基准测试, 耗时分析, 内存分析, 吞吐量, QPS, 瓶颈分析, 性能对比                                                                           |
| 项目知识图谱     | 为项目自动构建代码结构依赖图谱（节点+依赖边），跨模块改动/重构/审查时查依赖闭包与影响面，agent 开发时借全局视角理解项目、定位更准改动更稳；纯 agent 受众，不生成 mermaid 可视化                                          | 依赖图, 模块关系, 谁依赖, 影响面, 代码结构图谱, 画依赖图, 依赖分析, 改这个会影响哪些文件                                                                     |

> 你**不必背这 19 个技能**——说需求即自动匹配（见「使用方法」）。上表的作用是帮你快速了解「每个技能大概干什么、什么场景会自动触发」，方便你判断交付结果是否符合预期；想用得更好，扫一遍这张表即可，无需记忆触发词。

## 使用方法

通过 对话自然触发，说出需求即可自动匹配对应子技能。

**你不用记这 19 个子技能，也不用手动编排组合。** 只要把目标说清楚（最好带约束和验收，见「需求表达完整示例」），系统会按领域路由表 + 优先级矩阵**自动串联**所需的子技能与专项参考——例如你说"实现导出功能并出接口文档"，它会自动走 代码生成 + 文档生成；你说"定位这个报错顺带看看安全隐患"，它会自动走 Bug诊断 + 代码审查。组合是**自动发生的**，你只需描述完整目标。

Laravel、Eloquent、Blade、artisan、Migration、Form Request、Queue、PHPUnit、PHPStan 等关键词会触发 Laravel 专项参考；Java、Spring Boot、MyBatis、JPA、Maven、Gradle、JUnit、Mockito、JVM、GC、线程池、并发等关键词会触发 Java 专项参考；代码优化、性能优化、架构优化、N+1、缓存、异步、性能瓶颈等关键词会触发性能反模式审查与性能基准测试协同。专项参考与代码生成、测试用例生成、API设计、MySQL数据库、性能基准测试等现有子技能协同执行。

### 3 分钟上手

如果是第一次使用，不需要记住全部触发词，按下面入口说需求即可：

| 你想做什么         | 推荐说法                                          | 会进入                   |
| ------------------ | ------------------------------------------------- | ------------------------ |
| 写一个功能         | "帮我实现登录接口，要求有参数校验和测试"          | 代码生成 + 测试用例生成  |
| 修一个报错         | "这个报错帮我定位原因并给修复方案"                | Bug诊断                  |
| 检查代码有没有问题 | "审查这个文件，重点看安全和性能"                  | 代码审查                 |
| 做 CMS/PHP 二开    | "这是 WordPress/帝国CMS 项目，帮我加一个后台功能" | CMS二次开发              |
| 设计接口           | "设计一个订单导出接口，数据量大，需要进度条"      | API设计 + Init-Step-Poll |
| 换电脑继续上次任务 | "继续上次任务，先恢复 handoff"                    | 项目记忆管理             |
| 顺带做两件事       | "实现导出接口，顺带生成接口文档"                  | 代码生成 + 文档生成      |
| 不知道功能叫啥     | "帮我看看这段代码安不安全"                        | 代码审查（描述目标即可，不必记名字） |

### 需求表达完整示例（初次使用照着抄，不用背技能名）

光看表格还不够，下面给**真实可直接发送的句子**。记住一个万能公式：**目标 + 约束 + 验收**，越齐越省事（详见 FAQ 十六、Q"我不想被问太多"）。

**① 把"模糊需求"改成"可验收需求"（最推荐练手）**

- ❌ 太模糊：`帮我把系统优化一下` → 会触发 Wayfinder 探索，先和你对齐再动手（不是错，但慢）
- ✅ 直接命中：`用户列表接口响应超过 2s，帮我定位慢查询并加索引，目标降到 200ms 内` → 命中 `mysql-database` + `performance-benchmark`，且澄清少

**② 带约束的功能开发（目标 + 范围 + 格式 + 权限）**

- `给后台加一个导出用户的功能：范围=按筛选条件、格式=CSV、要鉴权+限频、能正确导出 1 万行且带表头` → 命中 `代码生成` + `doc-generation`，几乎不用追问

**③ 一次要两个能力（顺带式）**

- `实现登录接口，并生成单元测试` → `代码生成` + `测试用例生成`
- `定位这个报错，顺带看看附近代码有没有安全隐患` → `Bug诊断` + `代码审查`

**④ 不知道功能叫什么，只描述目标**

- `帮我看看这段代码有没有安全隐患` → 自动命中 `代码审查`（你无需知道 `@code-review` 这个名字）
- `这段逻辑太绕了，理一理结构` → 自动命中 `重构建议`

**⑤ 纠正 / 反馈（让下次更准）**

- `刚才那个修复不对，第 12 行的判空应该用 `if x is None` 而不是 `if not x`` → 触发修正并重跑验证；若排查耗时久，会被记入踩坑错误册供下次复用（见 FAQ 十七）

> 关键：**说目标比背名字更稳**。不确定叫啥就直接描述，系统按关键词 + 意图三分法路由；命中不了会问你一句，不会偷偷用错技能。

### ⚠️ 上手前先扫一眼红线（边界速览，完整版见 FAQ「能力边界速览 / 二、执行禁区 / 六、边界外」）

新手最容易"无意踩坑"的边界，先记一眼，免得做到一半才发现不能做：

- **本技能不覆盖的领域**：用户调研、工时排期、容器深度编排、IDE 配置、缺陷跟踪流程、安全深度扫描（只做边界说明，不替代专门流程）。
- **明确禁止的做法（执行禁区）**：直拼 SQL、Shell 写中文/UTF-8 文件、跨模块扩散修改、硬编码密钥、跳过验证直接交付、安全/数据类失败重试、凭猜测补业务规则、快速通道执行数据库写入、跨模块(≥2)/批量替换(>10处) 走快速通道。
- **关键限制**：单次最多加载 3 个 reference；子 Agent 禁止写/改代码（只做检索收集）；代码审查（`@code-review`）是**只读**的、不自动改写实现；Laravel / Java / JS 三个专项 reference 不支持 `@` 显式调用（用关键词触发即可）；涉及库写入 / 权限 / 生产配置须先给方案与回滚路径，不进快速通道。

> 记不住全表也没关系：**"写代码 / 查 Bug / 做文档 / 审质量"都能做；问调研排期、动生产配置前先确认、别让 Agent 替你盲写库"就是边界。**

### 文档阅读顺序

| 场景                       | 先看                                     | 再看                                  |
| -------------------------- | ---------------------------------------- | ------------------------------------- |
| 只想知道怎么用             | `README.md` 的"3 分钟上手"和"子技能列表" | `FAQ.md`                              |
| 不知道该用哪个技能         | `README.md` 子技能列表                   | `SKILL.md` 路由表                     |
| 遇到报错、卡住、看不懂提示 | `FAQ.md`                                 | 对应 `references/*.md` 的失败回退机制 |
| 长任务执行/续做/可靠交付   | `FAQ.md` 第九节                          | `SKILL.md` 长任务执行可靠性专节       |
| 要改技能执行规则           | `SKILL.md`                               | 对应 `references/*.md`                |
| 要看某个技能细节           | `references/` 下对应文件                 | `FAQ.md` 的反模式清单                 |
| 想先知道哪些不能做 / 红线 | `FAQ.md`「能力边界速览」/ 二、执行禁区 / 六、边界外 | `SKILL.md` 安全闸门 / 澄清策略 |                 |

### 组合子技能与进阶触发

- **不知道某个功能叫什么名字？** 不必背子技能名。路由表同时匹配「子技能名」和「功能说明里的场景词」，直接描述目标/动作即可：说"帮我看看这段代码有没有问题"会命中代码审查，说"这段逻辑太绕了理一理结构"会命中重构建议，说"写个带参数校验的接口"会命中代码生成。实在不确定就描述需求，系统按关键词 + 意图三分法路由，命中不了会向你确认，不会乱猜。
- **想一次用两个功能？** 多数情况**不用你操心组合**——只要把完整目标说清（如"实现导出功能并出接口文档"），系统按领域路由表 + 优先级矩阵**自动串联**所需子技能（代码生成 + 文档生成），你不必手动指定谁先谁后。两种可选表达仅当你想**精确控制**时再用：①「顺带式」显式点名（"...顺带生成接口文档"）；②「显式点名式」用多个 `@`（"`@code-review` 先审，`@refactoring` 再按问题重构"）。自动组合与显式调用都只跳过路由匹配、不影响协同加载。
- **组合的典型顺序**：审查类（代码审查 / Bug诊断）是只读的，先出报告、你确认后，再走重构 / 代码生成落地修改；性能类先跑基准拿基线、再重构，禁止无基线声称"显著提升"。多子技能同时命中按优先级矩阵组合路由（首选 + 必要协同），单次最多加载 3 个 reference，过多会提示你分阶段做。

## Hooks 自动守卫（可选，增强护栏）

本技能在 `hooks.json` 中提供一组**通用示例**守卫钩子（共 15 个：PreToolUse 3 + PostToolUse 11 + PreCompact 1），对全部子技能与 JS 专项共用，作为强制护栏兜底机械项（备份、lint、PHP8 兼容、安全/脱敏、UTF-8、调试残留、SELECT \*、压缩快照、规划拦截、受保护目录写前拦截）。

### 三个 hooks 文件的关系（模板 / 增量草案 / 安装产物）

目录里会出现三个带 `hooks` 前缀的 JSON，分工如下，别混为一谈：

| 文件 | 类别 | 由谁产生 | 作用 |
| --- | --- | --- | --- |
| `hooks.json` | **主模板（源，手写维护）** | 你自己维护 | 15 个跨平台守卫钩子的完整定义；占位符 `{{PYTHON_BIN}}`/`{{HOOKS_DIR}}` 由运行时或安装器替换。**已含** `capture_learning.py` 的 PostToolUse 项，但**不含** `UserPromptSubmit` 段 |
| `hooks.capture-draft.json` | **捕获 hook 增量草案（源，手写维护，可选）** | 你自己维护 | 同一个 `capture_learning.py` 的 PostToolUse 项 + **额外一条 `UserPromptSubmit`（带 `--mode correction` 直接捕获你的纠错句式，信号最准）**。因 `UserPromptSubmit` 并非所有 IDE 都支持（不支持的 IDE 会因未知事件名导致整份配置加载失败），故**单列 opt-in**，要用就单独并入，不用不影响主配置 |
| `hooks.installed.json` | **安装产物（自动生成，勿手改）** | `install_hooks.py` 生成 | 把 `hooks.json`（或指定源）里的占位符替换成真实机器路径后的可加载配置，直接接入运行时即可 |

一句话：**`.json` 是手写源、`capture-draft.json` 是可选附加源（多一路最准的纠错捕获）、`.installed.json` 是编译输出**。日常只动前两个源文件，第三个由安装器重跑覆盖。

**启用步骤**（两种方式任选其一）：

**方式 A：运行时占位符替换**（适用于支持变量替换的 IDE）

1. 将 `hooks.json` 接入你的 Agent 运行时（按各 IDE 的 hooks 配置入口加载）。
2. 设置两个环境变量：
   - `PYTHON_BIN`：Python 解释器路径（如 `/usr/bin/python3` 或 `F:\BtSoft\python\python_python\python3.exe`）
   - `HOOKS_DIR`：hook 脚本目录，可指向技能自带 `dev-expert/hooks/`，或你复制到项目的 `.codebuddy/hooks/`
3. `hooks.json` 命令串用 `{{PYTHON_BIN}} "{{HOOKS_DIR}}/xxx.py"` 占位符，加载时由运行时替换为真实路径——**不写死任何机器路径**，换机换项目直接改环境变量即可。

**方式 B：安装器预处理**（适用于运行时不支持占位符替换的 IDE，推荐跨平台使用）

1. 运行安装器，自动探测 Python 路径和 hooks 目录，生成已替换占位符的 `hooks.installed.json`：

   ```bash
   # 自动探测（推荐）
   python hooks/install_hooks.py

   # 或通过参数指定
   python hooks/install_hooks.py --python-bin /usr/bin/python3 --hooks-dir /path/to/hooks

   # 或通过环境变量指定
   PYTHON_BIN=/usr/bin/python3 HOOKS_DIR=/path/to/hooks python hooks/install_hooks.py
   ```

2. 将生成的 `hooks.installed.json` 接入你的 Agent 运行时（路径已硬编码，无需运行时替换）。
3. 换机换项目时重跑安装器即可；`--in-place` 可原地覆盖（自动备份为 `.bak`），但建议保留 `hooks.json` 模板不变，仅使用 `hooks.installed.json`。

> `hooks.installed.json` 文件顶部的 `_comment` 内含**各智能体平台适配说明**：CodeBuddy CN（工具名 `write_to_file`/`replace_in_file`）、Trae/Cursor 类（工具名 `Write`/`Edit`）等，matcher 已同时覆盖；若平台工具名不同（如 `MultiEdit`），在 matcher 里用 `|` 追加即可，无需改脚本。换机/换平台后 command 中的 Python 与 hooks 目录路径需同步更新（用安装器重生成或直接改 command）。

> hooks 是护栏不是验证替代：动态/业务正确性（真实运行、端到端）仍须 Agent 显式产出证据。hooks 拦截即视为该防线未过，禁止绕过；运行时无 hooks 集成时须回退正文手动执行。钩子明细与故障排查见 `FAQ.md` 十五、Hooks 自动守卫。

### 适配平台（多 IDE 兼容）

本技能对 hooks 的适配基于**工具名并集匹配（matcher）**，不是为每个 IDE 写专属配置。只要你的 Agent 运行时的工具名落在下表某个家族里，hooks 即开箱可用；工具名不同则在 matcher 用 `|` 追加一行即可，无需改脚本。

#### 平台适配矩阵

| 平台 | 工具名家族 | hooks 开箱覆盖 | 说明 |
| --- | --- | --- | --- |
| **CodeBuddy CN** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | 国内 IDE，代码/历史已确认 |
| **Trae / Trae CN** | `Write` / `Edit` | ✅ 已覆盖 | 代码/历史已确认 |
| **Cursor** | `Write` / `Edit` | ✅ 已覆盖 | 代码/历史已确认 |
| **Cline** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | 寄生 VS Code，搜索核实其工具名与 CodeBuddy 同族 |
| **Roo Code** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | Cline 分支，同族 |
| **Qoder CN** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | 国内 IDE，v1.8.2「同类产品适配」已登记 |
| **WorkBuddy** | `write_to_file` / `replace_in_file` | ✅ 已覆盖 | 国内 IDE，v1.8.2「同类产品适配」已登记 |
| **Claude Code** | `Write` / `Edit` / `Bash` / `UserPromptSubmit` | ✅ PostToolUse；`UserPromptSubmit` 可选 | 支持事件最全，搜索核实其 hooks 含 `PreToolUse`/`PostToolUse`/`UserPromptSubmit`/`Stop`/`Notification` |
| **Codex（OpenAI）** | `Bash` / 命令类 | ✅ 已覆盖 | 命令类家族 |
| **OpenClaw（龙虾类）** | 命令类 | ✅ 已覆盖 | `capture-draft.json` 明确点名可在 `UserPromptSubmit` 挂捕获 |
| **Gemini CLI** | `Bash` / 命令类 | ✅ 已覆盖 | 命令类家族，同 Claude/Codex 模式 |
| **Windsurf（Codeium）** | `write_file` / `edit_file` | ⚠️ 需 `|` 追加 | 工具名与主流不同，在 matcher 补 `write_file|edit_file` 即可 |
| **Zed** | 视配置 | ⚠️ 需确认 | 工具名随扩展形态变化，确认后追加 |
| **Continue** | VS Code 扩展 | ⚠️ 需确认工具名 | 确认其工具名后追加到 matcher |
| **Aider** | CLI 自有机制 | ❌ 非工具名匹配 | 走自带 hook / 包装层，不在本 matcher 范围 |

> ✅ = `hooks.json` matcher 已含该工具名家族，接入即生效；⚠️ = 在 matcher 用 `|` 追加对应工具名即可；❌ = 走另一套机制，本 hooks 不适用。

#### 怎么追加未列出的平台

若你的平台不在上表（或工具名不同，如 `MultiEdit`、`save_file`），只需编辑 `hooks.json` 每个 matcher 字符串，用 `|` 并入新工具名，例如把 `write_to_file|replace_in_file|Write|Edit` 改为 `write_to_file|replace_in_file|Write|Edit|MultiEdit|save_file`。**额外名称不会匹配时无害**，可放心并集。改完重跑安装器生成 `hooks.installed.json` 即可。

各平台适配细节也写在 `hooks.installed.json` 顶部的 `_comment` 里。本技能除 hooks 外对运行时不挑平台——**核心路由/18 子技能是纯自然语言触发的，不接 hooks 也能用**，hooks 只是可选增强护栏。

> ⚠️ **长任务 / 捕获 hook 要"自动执行 + 自动测试"须开放运行时权限**：`capture_learning.py`（学习捕获）与长任务闭环要自主跑通「执行命令 → 跑测试（`php -l` / `phpunit` / `node --check`）→ 落记录」，依赖运行时授予 `Bash` / `execute_command` 等工具的**免确认执行权限**。系统默认对危险操作（如**删除文件**、写入受保护目录、生产配置）会要求用户确认——未开放则长任务每步弹确认被卡死，自我改进闭环也无法自主推进。两层开放：① 技能侧 `SKILL.md` 的 `allowed-tools` 已声明 `Bash` 等工具；② 运行侧（IDE/平台权限策略）须允许这些工具 auto-approve（或任务前显式授权删除/写入等）。未开放时长任务须退化为「每步请求确认」模式，不得假设可无人值守自动执行（详见 `SKILL.md` frontmatter 的 `allowed-tools` 声明 与 `FAQ.md` 第九节）。

## 协同技能

### 子技能内部协同

> 下面 14 条协同路径是系统**自动执行**的编排结果——你描述完整目标后由领域路由表 + 优先级矩阵自动串联，**无需你手动拼接**。列出仅方便你了解内部如何协作、以及核对交付是否完整。你不必背这 19 个技能，说需求即自动匹配与组合。

19个子技能通过"关联Skill"章节相互引用，形成全生命周期闭环。常见协同路径：

- 通用软件项目：软件项目总控 → Spec驱动开发 → 技术选型/API设计/MySQL数据库/CMS二次开发 → 任务拆解与执行 → 代码生成 → 代码审查 → 测试用例生成 → 文档生成/部署运维说明 → 项目记忆管理
- 网站项目：网站项目总控 → Spec驱动开发 → 任务拆解与执行 → 前端设计/CMS二次开发/API设计/MySQL数据库 → 代码生成 → 代码审查 → 测试用例生成 → 文档生成 → 项目记忆管理
- 需求阶段：Spec驱动开发 → 任务拆解与执行 → 前端设计/代码生成
- 页面阶段：前端设计 → 代码生成 → 代码审查 → 测试用例生成 → 文档生成
- 交付阶段：代码生成 → 代码审查 → 测试用例生成 → 文档生成/部署运维说明
- 治理阶段：Bug诊断/重构建议 → 代码审查 → Karpathy编码规范 → 项目记忆管理
- CMS二开：CMS二次开发 → (前端设计/代码生成/Bug诊断/代码审查/技术选型) → 项目记忆管理
- MySQL专项：MySQL数据库 → 代码生成/代码审查/Bug诊断 → 测试用例生成 → 项目记忆管理
- 性能验证：性能基准测试 → 代码审查/重构建议/MySQL数据库 → 项目记忆管理
- 代码优化：代码审查(性能反模式) → 性能基准测试(L0/L1/L2) → MySQL数据库/重构建议 → 测试用例生成 → 项目记忆管理
- Laravel功能：Laravel专项参考 → 代码生成/API设计/MySQL数据库 → 代码审查 → 测试用例生成 + Laravel测试参考 → 项目记忆管理
- Java功能：Java专项参考 → 代码生成/API设计/MySQL数据库 → 代码审查 → 测试用例生成 → 性能基准测试/文档生成
- AJAX防卡死：Init → Step → Poll，API设计 → 前端设计 → CMS二次开发 → 测试用例生成
- 沉淀阶段：任何子技能 → 项目记忆管理（记录决策/规范/summary）

### 跨技能包协同

本技能包为独立套件，暂无可直接联动的其他职业技能包。如需在编程任务中集成外部数据或服务，可使用主 Agent 当前可用的外部检索工具获取。

## 版本

v1.11.16 | 更新日期: 2026-08-13

## 变更日志

### v1.11.16 (2026-08-13)

- 新增「项目知识图谱」子技能（`@project-knowledge-graph`）：为项目自动构建代码结构依赖图谱（节点 + include/use/autoload/extends/template/tpimport/import/cssimport/asset/calls 边），跨模块改动/重构/审查时查依赖闭包与影响面，agent 开发时借全局视角理解项目、定位更准改动更稳；纯 agent 受众，不生成 mermaid 可视化（人类兜底为 `graph.md`）
- 工具侧静态抽取 `scripts/build_graph.py`（纯正则，零 LLM token；LSP 仅探测可用性记录、抽取仍走正则）：输出 `{PROJECT_ROOT}/.ai-memory/knowledge-graph/{graph.json,meta.json,symbols.json,graph.md}`；内置抽取自校验（边目标反查剔除悬空边 + 符号孤儿仅告警不裁决 + 覆盖率报告）、查询子图裁剪（`--query` 支持逗号分隔多入口合并子图、`--direction/--depth`，默认 2 跳 + MAX_NODES=80 节点硬上限 + 环检测）、新鲜度校验（查时 mtime 粗筛 + 内容哈希精筛，过期触发重建）、冷启动（图不存在当场全量构建）、降级（构建失败回退临时 grep）
- SKILL.md 接入：路由表 + 子技能索引 + 优先级矩阵（+ 跨模块改动/重构/审查 先查图谱 协同行）；Step 2 钉 P1 规划前置依赖分析、Step 3 钉 P2 执行前局部影响面；`delivery-assurance.md` SELF-AUDIT 新增硬门禁 G1（grep 冲突以 grep 为准）/ G2'（图谱影响面须附 grep 实测证据，防 agent 谎报）/ G3（不可逆操作不单凭图谱，须 grep 复核 + 用户确认闸门）——任一不满足 SELF-AUDIT 判不通过、卡交付前
- 子技能总数 18 → 19；README 子技能列表/计数同步更新（历史变更日志条目保留原「18」不作回溯改写）

### v1.11.15 (2026-08-13)

- README「为什么保留渐进式路由」小节补充"为什么 SKILL.md 显得很大"：解释 SKILL.md 大而全是把"闭环步骤骨架 + 分发轨道 + 兜底护栏"刻意压在同一次加载里，门控拆散反而增加工作流断裂风险；真正可懒加载的细节都在 references/（26 文件专而深），SKILL.md 只保总控流程与跨步骤门控

### v1.11.14 (2026-08-13)

- README 新增「为什么保留渐进式路由（而非一步直达）」说明小节：解释 SKILL.md 未把 `@显式→关键词→领域路由表→优先级矩阵→意图三分法` 这套分层渐进路由抛离，是因为它是六步闭环工作流（Step 0–6）的入口分发轨道，每层都挂着后续一道门（澄清门控/路由边界拦截/组合协同顺序/安全闸门触发点），抛离会导致工作流断裂、丢失可验证/可恢复/可审计的闭环保证

### v1.11.13 (2026-08-13)

- 文档一致性收敛（审计「自动匹配+自动组合」后修正 2 处微瑕）：① README「协同技能」AJAX 协同链去掉多出的"代码生成"，与 SKILL.md 优先级矩阵（API设计+前端设计+CMS二次开发）对齐，消除符号/内容不一致；② FAQ 十八「组合套餐」原 4 条示例与 README「一句话触发对照表」重复 → 改为引用 README 主表，消除双份真相源

### v1.11.12 (2026-08-13)

- 按触发方式 4.5 用户反馈完善「组合自动」语义与子技能认知：① README 子技能列表后补定位说明"你不必背这 18 个技能——说需求即自动匹配"；② README「使用方法」补"你不用记子技能、也不用手动编排组合，组合是自动发生的，只需描述完整目标"；③ README「组合子技能与进阶触发」把"想一次用两个功能？"改为"多数情况不用你操心组合…自动串联"，顺带式/显式点名降为可选精确控制；④ README「协同技能」段顶部补"14 条协同路径是系统自动执行的结果…无需你手动拼接"；⑤ FAQ 十八「能力边界」补"组合是自动的，不用你手动编排"，组合套餐标注"系统自动触发"。统一降低"需手动编排组合"的暗示，强化"说目标即自动路由+自动串联"

### v1.11.11 (2026-08-13)

- 文档评审反馈补全（README/FAQ 人读完善）：① 填补"缺少完整操作示例"缺口——README「3 分钟上手」后新增「需求表达完整示例」小节，给 5 类可直接照抄的真实需求句子（模糊→可验收 / 带约束功能 / 顺带多技能 / 不知名字只说目标 / 纠正反馈），附万能公式"目标+约束+验收"；② 填补"FAQ 常见疑问覆盖不均、有些找不到答案"缺口——FAQ 新增「二十、新手高频疑问补遗」，回答 7 个此前无落点的问题（理解错怎么纠正 / 改错怎么回滚 `.bak` / 中文支持 / 口头纠正算不算反馈 / 省 token / 新手第一步 / 产出在哪看），并在顶部主题速查补第二十节指引

### v1.11.10 (2026-08-13)

- 真实多类型模拟审计（隔离 temp 项目跑通 Bug诊断→修复→测试、长任务 Wave1→handoff→新会话续做 Wave2、代码生成→测试协同 三条链路），暴露并修复 2 处静态审计查不出的运行中断点：① SKILL.md Step2「澄清策略分级（高/中/低）」仅被引用未定义 → 在 `references/execution-safety.md` 新增专节（三级判定标准 + 判定顺序 + 与意图三分法关系 + 反模式），SKILL.md 仅加锚点不膨胀；② Step0/Step6 的 `session_memory_{session-id}.jsonl` 的 `id` 生成规则未定义（恢复链隐患）→ 同文件补「session-id 生成规则」节（格式 `YYYYMMDD-HHmm` + 存 daily.md 顶部 + 读取定位逻辑）。长任务 handoff 续做与代码生成+测试协同链路经真实执行验证无结构性断点

### v1.11.9 (2026-08-13)

- README「适配平台」从一句话扩为**完整平台适配矩阵**：覆盖 CodeBuddy CN / Trae / Cursor / Cline / Roo Code / Qoder CN / WorkBuddy / Claude Code / Codex / OpenClaw（龙虾类）/ Gemini CLI（✅ 开箱覆盖）、Windsurf / Zed / Continue（⚠️ 需 `|` 追加工具名）、Aider（❌ 走另一套机制）；并诚实标注每项的覆盖状态与"怎么追加未列出平台"的方法。补回此前漏列的 Qoder CN / WorkBuddy（v1.8.2 适配却未在平台清单出现），并据搜索核实 Cline/Roo Code 与 CodeBuddy 同工具名族、Claude Code 支持 UserPromptSubmit 等事件

### v1.11.8 (2026-08-13)

- README/FAQ 完整性补齐（人读文档，求完善不求精简）：① 修复 2 处断裂交叉引用——FAQ 九 Q6 与 README 长任务权限提示曾指向已删除的「SKILL.md 权限前置注释」，改为指向 `SKILL.md` frontmatter 的 `allowed-tools` 声明 + `FAQ.md` 第九节；② README 文件结构补列 `hooks/` 目录（此前漏列，实际含 15 守卫钩子 + 安装器/检查器/提升评估脚本）；③ README Hooks 节新增「适配平台（多 IDE 兼容）」小节，说明 matcher 已覆盖 CodeBuddy/Trae/Cursor/Claude Code 等工具名变体；④ FAQ 顶部新增「主题速查」表（19 节导航）；⑤ FAQ 十五新增「如何禁用/卸载 hooks」Q；⑥ FAQ 十七新增「学习捕获钩子如何驱动自我改进」Q，把 capture→error-ledger→recurrence_promote 三层闭环讲清（Agent 不自动改规则，靠人把关）

### v1.11.7 (2026-08-13)

- 文档事实纠错（仅修错误，不删可读内容）：README/FAQ 是给人看的文档，故**保留全部原有可读内容**，只修正原文档本身写错的事实——① README hooks 计数 11→15（实际 PreToolUse 3 + PostToolUse 11 + PreCompact 1），与 FAQ 统一；② FAQ「三个专项 reference」修正为「四个」并补 `laravel-testing`（与实际 4 个专项 reference 一致）。注：README/FAQ 中的「18 个子技能」表述予以保留（子技能索引确为 18 项，对人读更具体），与 SKILL.md 正文「子技能总数」的写法存在轻微措辞差异，不影响理解

### v1.11.6 (2026-08-13)

- 补齐说明遗漏点：长任务要"自动执行 + 自动测试"（含捕获 hook 自我改进闭环）须运行时开放 `Bash`/`execute_command` 等工具的免确认执行权限——系统默认对删除文件、写入受保护目录、生产配置等危险操作要求用户确认，未开放会长任务每步弹确认被卡死。闭合到 `README.md` Hooks 节末提示与 `FAQ.md` 第九节；`SKILL.md` 正文不重复放置（避免 `#` 标题渲染为可见块），仅保留 frontmatter 的 `allowed-tools: Bash` 作为"技能需要此工具"的声明
- `SKILL.md` 的 `allowed-tools` 补充 `Bash`，声明技能需要该工具以驱动命令执行与测试

### v1.11.5 (2026-08-13)

- 修正 `recurrence_promote.py` 的 promote 落点混淆：原默认值 `主规则.mdc` 是某个具体项目的规则文件名（非 dev-expert 通用技能所有），已改为跨项目通用落点 `CLAUDE.md / AGENTS.md / project_memory.md（项目级记忆）`，并加 `--target` 覆盖说明；docstring 同步修正
- 修正 `recurrence_promote.py` 输出含 emoji（✅）在 Windows GBK 控制台导致 `UnicodeEncodeError` 崩溃：移除 emoji，改用 ASCII 标记 `[PROMOTE]`/`[skip]`，与现有 16 个防护 hook 的纯 ASCII 标签风格一致

### v1.11.4 (2026-08-13)

- 新增「学习捕获」hook（借鉴 elf-improving-agent 的捕获提醒理念，改写为 Python 兼容 Windows 与所有 Agent 工具）：`hooks/capture_learning.py` 挂 `PostToolUse`，监听工具输出错误信号（elf 16 个 + dev-expert 语境扩展：Parse error / PHP Fatal / 断言失败 / GATE-CHECK 不足…）与用户输入纠错句式（中英文），命中即回显「建议记录到 error-ledger」提醒，扫描 `error_index.md` 做 Recurrence 去重提示；非阻塞、`exit 0` 仅提醒、错误处理 `exit 1`（仍不阻断），不自动写文件（遵循 error-ledger 禁忌）
- 新增 `hooks/recurrence_promote.py`：解析单条 `ERR-XXX.md` 的 `Recurrence-Count/Tasks/First-Seen/Last-Seen` 字段，评估硬规则（Recurrence-Count>=3 且 Tasks>=2 且 30 天窗口）输出 promote 建议，不自动改写规则文件
- `references/error-ledger.md` 单条模板新增 `Recurrence-Count/First-Seen/Last-Seen/Tasks/Pattern-Key` 5 字段 + 索引模板新增 `Recurrence-Count` 列，支撑 Recurrence 自动评估（缺字段时 `recurrence_promote.py` 优雅跳过）
- `hooks.json` 的 `PostToolUse` 段合并 `capture_learning.py`（matcher 并集覆盖 `write_to_file|replace_in_file|Write|Edit|Bash|execute_command|terminal…`），现有 10 个防护 hook 不受影响；重跑 `install_hooks.py` 生成的 `hooks.installed.json` 路径已正确指向 dev-expert/hooks（修正此前误指 `Trae_Date` 旧路径）。未并入 `UserPromptSubmit` 段（CodeBuddy 系可能不支持该事件名，避免配置加载失败）

### v1.11.3 (2026-08-13)

- 新增 `references/style-alignment.md`「风格嗅探协议」：解决二开/插件开发时 Agent 凭自身想象自由发挥模板样式的问题——生成/修改前强制先取样原项目代表性已有文件，提取缩进/开标签/括号位置/数组键引号/模板变量命名/PHP-HTML 混编等风格标记，产出「风格基线」块，生成代码逐行对齐；仅当项目空白无参照才回退默认约定并标注
- `code-generation.md` 第三步需求分析挂钩风格嗅探：二开/插件场景强制先读原项目文件再生成，禁止凭想象套用风格
- `cms-development.md` 第七步由"声明风格优先级"改为"先嗅探原项目代表文件→再套用"，内置命名表降为兜底默认值
- 补齐缺失的 `hooks.json` 参数化模板（带 `{{PYTHON_BIN}}`/`{{HOOKS_DIR}}` 占位符），使方式 A 占位符替换与安装器 `install_hooks.py` 方式 B 均可一键生成 `hooks.installed.json`（此前模板缺失导致两条启用路径均不可用）

### v1.11.2 (2026-08-12)

- README「3 分钟上手」后新增「⚠️ 上手前先扫一眼红线（边界速览）」块：把"不覆盖领域 / 执行禁区 / 关键限制"从 FAQ 上提到 README 入口，新手无需翻 FAQ 即可看到边界；「文档阅读顺序」表同步补"想先知道哪些不能做"一行指向 FAQ 速览

### v1.11.1 (2026-08-12)

- README「3 分钟上手」新增两行（顺带做两件事 / 不知道功能叫啥），并新增「组合子技能与进阶触发」小节：说明不知道功能名时直接描述目标、一次用两个功能的「顺带式 / 显式点名式」表达、组合的典型顺序与 3-reference 上限
- FAQ 新增第十八节「子技能组合与触发进阶」：澄清代码审查 + 重构等组合能否同时用、怎么配合（先审查后重构 / 审计修复分离）、常见组合套餐、不知功能名与双功能组合的触发表达

### v1.11.0 (2026-08-11)

- allowed-tools 补充 Task（子 Agent）工具：与 SKILL.md L438 子 Agent 边界声明对齐，长任务可委派子 Agent 并行处理
- allowed-tools 补充 WebSearch 工具：编程场景支持查最新文档、API 参考、解决方案
- 新增 `hooks/dep_scan.py`：依赖文件变更后提示漏洞扫描命令（npm audit / pip-audit / composer audit / govulncheck / mvn dependency-check / bundle audit），覆盖 16 种依赖清单文件
- 新增 `hooks/sql_injection_check.py`：SQL 注入风险检查，覆盖 7 种风险模式（PHP $_GET/$_POST 直接入 SQL、PHP 字符串拼接、PHP 变量插值、Python f-string、Python % 格式化、JS 模板字符串、Java 字符串拼接），支持 9 种安全模式识别（prepare/bindParam/bindValue/ORM 等），13 项测试全通过
- hooks.json 注册 dep_scan 和 sql_injection_check 为 PostToolUse hook
- 全技能表格对齐空格压缩优化：SKILL.md + 13 个 reference 文件，合计节省约 6,900 token，零语义损失

### v1.10.0 (2026-08-11)

- 补齐 CodeBuddy Rules 覆盖时缺失的 14 项规则机制，对标对表逐项落地：
  - 新增 `delivery-assurance.md`：执行率自检（SELF-AUDIT 11 条）、收尾报告模板（5 字段强制格式）、确认超时默认规则、Graceful Abort 流程
  - 新增 `error-ledger.md`：踩坑错误册 ERR-XXX 系统（索引 + 单条模板 + 触发-定位-读取流程 + 新坑即录 + 归档策略）
  - 新增 `execution-safety.md`：规划门禁（PLAN-GATE 15 项）、写码前实码确认（读文件+搜关联+冲突检查）、审计修复分离（两阶段不交叉）、不卡死计数器（≥3 次列替代方案）、批量修改 7 防线（预检→试点→备份→执行→后检→MD5→回读）、清单化质量自审 10 条、安全红线清单 10 条
- SKILL.md 六步闭环各 Step 同步接入新 reference：
  - Step 2：规划门禁（PLAN-GATE）强制打勾，Trivial Fix 可跳过
  - Step 3：写码前实码确认 / 审计修复分离 / 不卡死计数器 / 批量修改 7 防线 / 清单化质量自审+安全红线
  - Step 4：清单化验证（质量 10 条 + 安全红线 10 条）+ PHP 内联 JS 三道强制校验
  - Step 5：执行率自检 + 收尾报告模板 + 确认超时默认 + Graceful Abort
  - Step 6：踩坑错误册更新（新坑即录 + Bug 诊断/审查/重构 session 启动时查索引匹配）
- FAQ 新增第十七节「交付保障与踩坑管理」6 条 Q&A
- README 文件结构同步 3 个新 reference

### v1.9.0 (2026-08-11)

- 新增 Step 1.5「需求澄清门控」：复杂任务强制执行，将模糊形容词（快/稳定/安全/好用）转为可验收标准，支持验收口径对齐与假设显式化
- 新增 Wayfinder 模式：大型模糊任务（如"提升性能""整理代码"）的探索路径——现状快照→问题树展开→候选排序→最小探索→收敛为明确任务
- code-generation 新增第〇步：TDD 与审查链前置决策——复杂任务在 Spec 检查前自动决策联动 test-generation 和 code-review
- project-memory-management 新增第三步点六：术语表维护（Glossary）——术语漂移自动记录规范名称，新会话加载确保跨轮统一
- software-project 新增第三步点五：模块边界审查——5 维审查（依赖方向/接口契约/数据持有/变更半径/术语一致性），循环依赖为阻塞级
- frontend-design 新增第二步点五：快速原型与草图——ASCII 线框图快速对齐页面骨架和交互流，确认结构后再进入完整视觉设计
- FAQ 新增第十六节「需求澄清与模块边界」，覆盖门控/wayfinder/边界审查/TDD链/术语表/快速原型 6 问

### v1.8.4 (2026-08-10)

- JavaScript 专项参考完整性维护：① 审查修复 FAQ 悬空 `fix_js_code()` 引用、Node 下限统一 ≥15；② 补充「CMS / PHP 内联 JS 专项」三道强制校验（HTML 事件属性引号配对 / window.open features 非空收尾 / 批量改造后全仓 Node 校验）；③ 按二开场景裁剪：移除 9 种设计模式整节、JSDoc 整节、Node 专属生产坑（文件 749→262 行）；④ 补全 FAQ 七节 Q5 专项 reference 引用一致性（含 `javascript-development`）；⑤ 备份文件移出 `references/`
- SKILL.md 领域路由表（JS 关键词含 PHP 内联 JS/window.open/onclick 事件属性）、优先级矩阵、协同顺序规则同步对齐 JS 链路

### v1.8.3 (2026-08-10)

- 新增「JavaScript 专项开发参考」（`references/javascript-development.md`）：整合 JS 代码质量检查（Node.js 4 步工作流：版本检查→语法检查→修复→验证）、9 种 GoF 设计模式、Google JS Style Guide（47 条规则 8 分类摘要）、JSDoc 文档注释规范、常见生产坑；**含「CMS / PHP 内联 JS 专项」小节**——固化 PHP 混编文件内 `php -l` 漏检 JS 的三道强制校验
- SKILL.md 领域路由表、专项 reference 映射、优先级矩阵和协同顺序规则同步追加 JS/Node.js 链路

### v1.8.2 (2026-08-10)

- 新增「同类产品适配」专节：覆盖 CodeBuddy CN / Trae CN / Qoder CN / WorkBuddy 四平台适配矩阵、跨平台使用指南和平台无关能力清单；FAQ 新增「十五、同类产品适配」问答

### v1.8.1 (2026-08-10)

- 新增「国内云服务适配」专节：覆盖阿里云/腾讯云/华为云部署、存储、数据库、容器、CDN、Serverless 等场景路由与 IaC 推荐；FAQ 新增「十四、国内云服务适配」问答

### v1.8.0 (2026-08-10)

- 融合 ClawMemory 写后即记协议：每次实质性操作（Bug修复/功能实现/重构/决策定案等）完成后立即追加 `daily.md`（append-only），不等待会话结束
- 新增 Step 0「工作记忆加载」：新会话启用写后即记上下文，7 类触发条件自动追加当日操作日志
- 新增记忆维护协议：`daily.md` 超 8000 字符精简提醒，超 12000 字符强制蒸馏；>30 天日志目录自动蒸馏入 `project_memory.md` 后清理
- 新增记忆生命周期流转：daily.md → session_memory → project_memory → user_profile

### v1.7.11 (2026-08-09)

- 新增「二、子Agent 边界与委派协议」专节（L0 级）：子Agent 分类与定位、核心禁令（禁改码/方案须复核/不继承铁律）、检索收集型输出规范、委派前置条件、边界外禁止、与主流程衔接；FAQ 新增「八、子Agent 边界」问答
- 新增「长任务执行可靠性（L0）」专节：澄清轮次上限仅约束单 Wave 收敛循环（不跨 Wave 累计、已验证产出物不回退清零）、周期检查点（handoff.md/状态文件）、两层进度验证、可靠交付物四要素强制披露；验收标准新增「长任务可靠」维度，模板化交付新增未验证项强制披露条款
- 收敛 SKILL.md 过度叙事描述，保留全部规则、表格、参数与交叉引用

### v1.7.10 (2026-08-07)

- 全包完整性审计：18 个子技能 reference + 3 个专项 reference（laravel-development / laravel-testing / java-development）全部齐备；SKILL.md / README.md / FAQ.md 中全部 `references/*.md` 链接零断链；主流程 6 步跨文件引用的 7 处步骤号（software-project 第六步、code-generation 第六步、bug-diagnosis 第七步、website-project 第七步、frontend-design 第十步、cms-development 第八步、project-memory-management 第五步）全部命中目标文件；18 个子技能均含「失败回退机制」表——任务可端到端执行交付，无断点。
- 子任务质量审计：18 个子技能均具备「输入要求 / 输出格式 / 质量标准 / 失败回退机制」四大质量支柱；质量标准为可核查硬约束（api-design 7 项规范验证清单、test-generation 强制安全/性能/长任务覆盖、bug-diagnosis 根因须有验证证据且禁止猜测）；跨子技能质量协同一致（Spec 前置闸门、Karpathy 精准修改、Init-Step-Poll 长任务契约、安全/性能覆盖）——每个子任务可独立交付高质量产物，无质量断点。

### v1.7.9 (2026-07-10)

- 高频 reference 补充实战请求示例：Bug诊断、代码审查、API设计、测试用例生成、CMS二次开发
- 示例统一说明输入、约束、安全/验证要求和优先协同 reference，降低新手照做成本
- 保持 18 个正式子技能数量不变，新增内容仅作为现有 reference 的使用引导

### v1.7.8 (2026-07-10)

- README 新增 3 分钟上手和文档阅读顺序，降低初次使用门槛
- FAQ 新增普通人可读错误说明、网络重试边界、常见反模式与踩坑汇总
- SKILL.md 新增错误提示可读性规则和网络重试规则
- code-generation.md 新增贴近实际场景的功能实现请求示例

### v1.7.7 (2026-07-10)

- project-memory-management.md 新增换机/换 IDE 交接协议（Handoff Protocol）
- 新增 `.ai-memory/handoff.md` 可提交交接文件，支持旧电脑收尾、新电脑恢复未完成主线任务
- 记忆恢复策略优先加载 Handoff Checkpoint，避免依赖旧 IDE 会话和临时缓存

### v1.7.6 (2026-07-10)

- SKILL.md FAQ 链接同步改为 `./FAQ.md`
- references/ 目录继续只承载 18 个子技能模板和专项 reference

### v1.7.5 (2026-07-10)

- bug-diagnosis.md 新增推断交叉验证规则，要求候选根因必须有日志、复现、源码、版本、官方文档或运行证据支撑
- doc-generation.md 新增引用来源与溯源格式，要求关键结论可追到代码、Spec、API、配置、测试或官方文档
- spec-driven-development.md 新增模糊需求深挖与边界案例，将"快速/稳定/安全/兼容/优化"等表述转为可验收标准

### v1.7.4 (2026-07-10)

- performance-benchmark.md 新增自动化扫描档位、L0/L1/L2 分层分析、硬性性能反模式和优化策略模板
- code-review.md 新增性能反模式审查清单，覆盖 N+1、阻塞 I/O、无界缓存、无上限拉取和索引失效
- SKILL.md 增加代码优化/性能优化/N+1/缓存/异步相关路由，要求先定位嫌疑点再用 benchmark/profile/EXPLAIN 验证

### v1.7.3 (2026-07-10)

- SKILL.md 增加 Java / Spring 领域路由、优先级矩阵和协同路径
- code-review.md 新增 Java 专项审查清单，覆盖正确性、安全、性能、健壮性、并发、Spring/JVM 风险
- 保持 18 个子技能不变，Java 专项参考不作为独立 `@` 显式调用标识

### v1.7.2 (2026-07-10)

- 新增小片段快速审查模式：代码规范与可读性、潜在 Bug、性能分析、安全性考量四象限
- 新增"未发现明显问题"输出规范，要求说明已覆盖维度、残余风险和建议验证

### v1.7.1 (2026-07-10)

- 新增 Laravel 测试专项参考：`references/laravel-testing.md`
- SKILL.md 增加 Laravel / PHP框架领域路由、优先级矩阵和协同路径
- 保持 18 个子技能不变，Laravel 专项参考不作为独立 `@` 显式调用标识

### v1.7.0 (2026-07-04)

- frontend-design.md 大幅增强：吸收企业级前端工程规范（来自 frontend-spec）
- 第四步新增 CSS/SCSS 工程约束：嵌套深度 ≤3、z-index 统一管理、单位优先级、公共样式抽离、禁止硬编码颜色
- 第七步升级为「可访问性 + 安全性 + 可用性」三步检查：XSS/CSRF/敏感信息/接口权限/第三方脚本 5 条安全红线
- 第八步新增 5 个子章节：项目目录规范、命名规范、代码质量基线（JS/TS/Vue/React）、ESLint/Prettier 基线、性能实现规范
- 质量标准追加 5 条新约束（CSS 工程/安全/命名/TS 类型/ESLint）
- 验证清单追加安全性检查项
- README 子技能表同步扩展前端设计关键词

### v1.6.0 (2026-07-04)

- 新增 性能基准测试 子技能（references/performance-benchmark.md）
- 覆盖量化性能验证：识别触发面、耗时/内存/吞吐量测量、瓶颈报告、A/B对比
- cms-development.md 第三步对齐 mysql-database.md 引擎推荐：默认 InnoDB，MyISAM 仅历史遗留
- performance-benchmark.md 补充 软件项目总控、网站项目总控 为可选协同引用
- task-decomposition-and-execution.md XML 模板 `<security>` 节点标注"禁止留空"，质量标准同步补强
- SKILL.md 优先级矩阵补全3条缺失条目：Spec驱动开发、Karpathy编码规范、任务拆解与执行
- 修复3对单向引用：website-project → software-project、code-review → code-generation、tech-selection → software-project
- 更新子技能数量 17 → 18

### v1.5.1 (2026-07-02)

- 任务拆解模板新增安全触发面识别，Wave 任务必须写明安全验证项
- SKILL.md 新增部署、发布、回滚、运维、监控、告警、巡检路由
- 软件项目总控补强监控指标、告警阈值、巡检清单和运维交付材料
- 测试用例生成补齐安全测试、性能测试和 Init-Step-Poll 长任务测试分类

### v1.5.0 (2026-07-02)

- 新增 软件项目总控 子技能（references/software-project.md）
- 覆盖 API 服务、后台模块、插件、CLI 工具、数据脚本、自动化任务等非网站项目的完整交付链
- 修正组合路由规则：多子技能命中时先按优先级矩阵组合路由，无法组合时才选最高匹配度
- 补强任务拆解关联链和项目记忆流程格式
- 更新子技能数量 16 → 17

### v1.4.1 (2026-07-02)

- 强化 MySQL 索引策略：查询路径、联合索引顺序、覆盖索引、分页、JOIN、ORDER BY/GROUP BY、冗余索引治理、写入成本和 EXPLAIN 验收
- 更新 MySQL数据库输出格式，要求说明字段顺序理由、覆盖查询、写入成本和回滚 SQL
- 更新代码审查清单，新增 MySQL 索引审查维度

### v1.4.0 (2026-07-02)

- 新增 MySQL数据库 子技能（references/mysql-database.md）
- 覆盖表结构设计、SQL安全、索引设计、事务边界、慢查询诊断、迁移回滚、数据安全和 PHP/CMS 数据访问约束
- SKILL.md/README.md 新增 MySQL 路由关键词、子技能索引、优先级矩阵和协同路径
- 更新子技能数量 15 → 16

### v1.3.3 (2026-07-02)

- 补充 AJAX 渐进式防卡死架构：`Init → Step → Poll`
- 在 CMS二次开发、API设计、前端设计、网站项目总控中加入长任务防卡死规则
- 补充 `AJAX防卡死 / Init-Step-Poll / 长任务 / 轮询` 路由关键词

### v1.3.2 (2026-07-02)

- 统一 5 个子技能的执行流程步骤名与失败回退表步骤名
- 修复 `spec-driven-development.md` 输出示例二级标题被误识别为真实章节的问题
- 复测 15 个 references 索引、必需章节、代码块和回退表一致性

### v1.3.1 (2026-07-02)

- 将 `ui-ux-pro-max-zh.md` 的高价值规则吸收到前端设计子技能
- 补充设计思维、色板、字体配对、品牌规范、Banner、图标、社媒图和设计资产规格
- 更新前端设计路由关键词：品牌设计、Banner、图标、社媒图

### v1.3.0 (2026-07-02)

- 新增 网站项目总控 子技能（references/website-project.md）
- 补齐完整网站项目生命周期：项目启动、站点规划、内容SEO、前端设计、CMS/API/数据、任务Wave、测试安全、性能部署、验收交接、运维沉淀
- 建站类需求拆解前强制先调用网站项目总控

### v1.2.0 (2026-07-02)

- 补齐前端设计能力缺口，新增 前端设计 子技能（references/frontend-design.md）
- 前端设计流程覆盖：需求与场景分析、信息架构、视觉设计系统、交互状态、响应式兼容、可访问性、前端实现方案、浏览器验证、项目记忆沉淀
- SKILL.md 新增前端设计路由、子技能索引、优先级矩阵和协同路径
- 更新子技能数量 13 → 14

### v1.1.0 (2026-07-02)

- 新增 CMS二次开发 子技能（references/cms-development.md）
- 补充 CMS 探测、PHP 版本选型、数据库规范、PHP8兼容、安全红线、插件开发、代码风格、交付检查、记录沉淀
- code-generation.md、bug-diagnosis.md、code-review.md、tech-selection.md 补充 CMS 专项指引
- SKILL.md/README.md 新增 CMS 子技能路由、索引、优先级矩阵、协同路径
- 更新子技能数量 12 → 13

### v1.0.3 (2026-07-02)

- 修复 bug-diagnosis、code-generation、code-review 失败回退表步骤名与执行流程错位
- 修复 SKILL.md 工具名引用错误：`Read` → `Read`
- 补全 spec-driven-development、task-decomposition-and-execution 的「记录到项目记忆」步骤及回退行
- 统一 SKILL.md 与 README.md 治理阶段协同路径描述

### v1.0.2 (2026-07-02)

- 修复 spec-driven-development.md 章节编号断裂与代码块嵌套解析异常
- 修复 tech-selection.md 连接器章节位置错误
- 为多个缺失子技能补全失败回退机制表
- 补全 code-generation.md、code-review.md 的「记录到项目记忆」步骤
- 新增子技能优先级矩阵和 `.gitignore`

### v1.0.1 (2026-06-19)

- 对齐 description 子技能名与路由表名称
- 压缩路由表说明列
- 新增跨技能协同指引章节
- 删除冗余英文 description 行

### v1.0.0 (2026-06-15)

- 初始发布，含 12 个子技能：API设计、Bug诊断、代码生成、代码审查、重构建议、测试用例生成、技术选型、文档生成、任务拆解与执行、Spec驱动开发、Karpathy编码规范、项目记忆管理
- 建立 references/ 目录隔离子技能模板
- 引入 Karpathy 编码哲学、Wave 执行模式和 Spec 驱动开发 artifact flow

## 文件结构

- `SKILL.md` - 技能运行时指令
- `README.md` - 本文件，用户入口文档
- `FAQ.md` - 常见问题、执行禁区、验证失败和边界外请求答疑
- `hooks/` - 钩子脚本目录：15 个守卫钩子（备份/lint/PHP8/安全/脱敏/UTF-8/调试残留/SELECT \*/依赖扫描/SQL注入/CMS风险/学习捕获/压缩快照/规划拦截/受保护目录拦截）+ `install_hooks.py` 安装器 + `step_ref_check.py` 步骤号检查器 + `recurrence_promote.py` 提升评估
- `scripts/build_graph.py` - 项目知识图谱构建/查询工具（**纯正则，无 AST/tree-sitter**；LSP 仅探测可用性记录、不参与抽取；构建与查询均**零 LLM token**）：`--root` 全量构建 / `--query <file|symbol，多入口逗号分隔合并子图> [--direction up|down|both] [--depth N]` 子图裁剪 / `--rebuild` / `--incremental` / `--selftest`；输出写盘 `{PROJECT_ROOT}/.ai-memory/knowledge-graph/{graph.json,meta.json,symbols.json,graph.md}`。token 消耗对比见文末「附录 A」
- `references/` - 子技能详细模板（共19个子技能）+ 4 个专项 reference（不计入子技能）+ 3 个工作流保障 reference
- `references/laravel-development.md` - Laravel 开发专项参考（不计入子技能）
- `references/laravel-testing.md` - Laravel 测试专项参考（不计入子技能）
- `references/java-development.md` - Java/Spring 开发专项参考（不计入子技能）
- `references/javascript-development.md` - JavaScript/Node.js 开发专项参考（不计入子技能）；含「CMS / PHP 内联 JS 专项」：PHP 内联 JS 强制校验（引号配对 / window.open features 收尾 / 全仓 Node 校验）
- `references/delivery-assurance.md` - 交付保障：执行率自检 / 收尾报告 / 确认超时 / Graceful Abort
- `references/error-ledger.md` - 踩坑错误册：ERR-XXX 索引 + 单条模板 + 触发-定位-读取 + 新坑即录 + 归档
- `references/execution-safety.md` - 执行安全：规划门禁 / 审计修复分离 / 批量修改防线 / 写码前确认 / 不卡死计数器 / 清单化质量+安全
- `references/style-alignment.md` - 风格对齐（风格嗅探协议）：二开/插件生成前强制取样原项目已有文件、提取风格标记、产出「风格基线」逐行对齐，禁止凭想象套用样式

## 维护建议

### Reference 体量监控

单个 reference 文件建议控制在 **400 行以内**；超过时考虑拆分（如「设计规范」与「实现规范」分离）或提取共性内容到独立 reference。当前体量分布（按行数降序）：

| 文件                         | 行数   | 评估                                       |
| ---------------------------- | ------ | ------------------------------------------ |
| project-memory-management.md | ~479   | 偏大，职责内聚可暂保留                     |
| frontend-design.md           | ~435   | 偏大，后续可拆分「设计规范」与「实现规范」 |
| cms-development.md           | ~406   | 偏大，CMS 场景复杂度本身高                 |
| code-review.md               | ~309   | 合理                                       |
| 其余 21 个                   | 84-281 | 健康                                       |

### 跨文件步骤号一致性检查

新增/修改 reference 章节号后，运行检查器验证 SKILL.md / README.md / FAQ.md 中的步骤号引用与目标文件实际章节一致：

```bash
python hooks/step_ref_check.py
```

退出码 0 = 全部匹配；1 = 发现不匹配（会列出具体位置和期望/实际步骤号）。建议在合并 PR 前或重大版本发布前运行。

---

## 附录 A：知识图谱 token 消耗对比（常规 LLM 理解 vs 图谱方式）

> 估算量级，非精确计费；基准：332 文件 / ~5 万行帝国 CMS 项目，图含 2890 有效依赖边，`MAX_NODES=80`（节点硬上限）。

| 维度 | 常规 LLM 理解（无图谱） | 知识图谱方式 |
|------|------------------------|-------------|
| 构建 / 索引成本 | 无（每次现读源码） | **0 token**（纯正则本地抽取，不进 LLM 上下文） |
| 单次依赖查询 | 6k–60k token（把 5–50 个源文件喂进上下文理解依赖） | **1k–3k token**（返回子图 JSON，≤80 节点） |
| 10 次任务累积 | 60k–600k token | 10k–30k token |
| 跨会话复用 | 每次重读，不留存 | 图谱缓存复用，query 恒定 ~2k |
| 上下文污染 | 大（源码占满上下文窗口） | 小（仅依赖拓扑，不含实现细节） |

单次跨模块依赖查询的 token 消耗（ASCII 示意，取中值）：

```
常规 LLM 理解（无图谱）
  读 10–50 个源文件理解依赖    ████████████████████████   6k – 60k tok
知识图谱方式
  返回子图 JSON（≤80 节点）     ██                         ~1k – 3k tok

→ 单次节省约 70%–95%；跨会话 / 多任务累积节省更显著（图谱一次构建、永久复用）
```

**为何能省**：图谱把"代码 → 依赖关系"的抽取放在 LLM 之外（纯正则静态抽取，LSP 仅探测可用性、不参与抽取），LLM 只需消费精简后的依赖拓扑 JSON，而非原始源码。构建阶段 token≈0、查询阶段不重读源码，故整体近零 LLM 成本。详见 `references/project-knowledge-graph.md`。