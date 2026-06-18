---
name: dev-expert
description:
  编程专家技能套件：API设计、Bug诊断、代码生成、代码审查、重构建议、测试用例生成、技术选型、文档生成、任务拆解与执行、Spec驱动开发、Karpathy编码规范、项目记忆管理。
  API设计: API设计, RESTful, GraphQL, 接口规范; Bug诊断: Bug诊断, debug, 报错, 异常堆栈; 代码生成: 代码生成, 生成代码, 实现功能, 写代码; 代码审查: 代码审查, code review, 代码异味, 安全漏洞; 重构建议: 重构建议, 重构, 坏味道, 可维护性; 测试用例生成: 测试用例生成, 单元测试, 测试用例, 集成测试; 技术选型: 技术选型, 技术栈, 框架选型, 技术评估; 文档生成: 文档生成, API文档, README, 技术文档; 任务拆解与执行: 任务拆解与执行, 任务分解, Wave执行, 子任务; Spec驱动开发: Spec驱动开发, spec, 需求对齐, 需求规格; Karpathy编码规范: Karpathy编码规范, Karpathy, 编码哲学, 简洁优先; 项目记忆管理: 项目记忆管理, 项目记忆, 跨会话, 上下文沉淀。
version: "1.0.1"
author: "智慧半岛"
---

# dev-expert -- 编程专家综合技能

本技能是一个综合技能套件，包含多个子技能。接到用户请求后，按以下流程执行。

## 执行流程

### Step 1: 意图识别与路由匹配

分析用户输入，与下方路由表逐一比对。匹配规则：
- 用户输入中包含路由表中「子技能」列的关键词 → 匹配该子技能
- 用户输入中包含路由表中「功能说明」列中提到的场景 → 匹配该子技能
- 多个子技能同时匹配时，选择匹配度最高的
- 无法唯一确定时，向用户确认意图

### Step 2: 加载子技能模板

匹配到子技能后，根据子技能索引表找到对应的文件路径，**必须**使用 `read_text` 工具读取 `references/` 目录下的完整执行模板。

### Step 3: 按模板执行

严格按照加载的模板逐步执行。模板中定义了：
- 输入要求（用户需要提供什么）
- 执行步骤（每一步做什么、如何判断）
- 输出格式（最终产出的结构和规范）
- 质量标准（产出必须满足的底线）

### Step 4: 输出结果

按模板规定的格式输出结果。如果模板要求生成文件，写入后声明产出物。

## 约束规则

1. **必须先读模板再执行**：匹配到子技能后，严禁凭记忆或猜测执行，必须先读取对应的 references 文件
2. **严格遵循模板**：不得跳过步骤、不得省略检查项、不得自行简化流程
3. **输入不足时主动索取**：模板中标注「必填」的输入项缺失时，向用户索取
4. **质量底线不妥协**：模板中的质量标准必须逐条满足

## 路由表

| 子技能 | 功能说明 |
|--------|----------|
| API设计 | 根据业务需求设计RESTful或GraphQL API接口... |
| Bug诊断 | 分析错误日志、异常堆栈和代码，定位Bug根因并给出修复方案。 |
| Karpathy编码规范 | 提供Andrej Karpathy提出的4条核心编码哲学：编码前思考、简洁优... |
| Spec驱动开发 | 在编码前对齐需求规格，使用OpenSpec的artifact flow和de... |
| 代码审查 | 审查代码质量，发现潜在Bug、安全漏洞、性能问题和代码异味... |
| 代码生成 | 根据功能需求生成高质量代码实现，支持多种编程语言和框架，包含错误处理和边界条件。 |
| 任务拆解与执行 | 将复杂编程需求拆分为原子任务，按依赖关系分组为Wave执行，每个任务独立上下文... |
| 技术选型 | 根据项目需求、团队能力和约束条件，推荐合适的技术栈、框架和工具... |
| 文档生成 | 根据代码生成技术文档，包括函数文档、README、API文档和架构说明... |
| 测试用例生成 | 根据代码逻辑生成单元测试、集成测试和边界条件测试，覆盖正常路径和异常路径。 |
| 重构建议 | 分析代码结构，识别坏味道，提供具体的重构方案和步骤，提升代码可维护性。 |
| 项目记忆管理 | 捕获会话上下文、技术决策和项目规范，实现跨会话项目记忆沉淀与恢复。 |

## 子技能索引

| 子技能 | 英文标识 | 文件 |
|--------|----------|------|
| API设计 | `api-design` | [references/api-design.md](./references/api-design.md) |
| Bug诊断 | `bug-diagnosis` | [references/bug-diagnosis.md](./references/bug-diagnosis.md) |
| Karpathy编码规范 | `karpathy-coding-guidelines` | [references/karpathy-coding-guidelines.md](./references/karpathy-coding-guidelines.md) |
| Spec驱动开发 | `spec-driven-development` | [references/spec-driven-development.md](./references/spec-driven-development.md) |
| 代码审查 | `code-review` | [references/code-review.md](./references/code-review.md) |
| 代码生成 | `code-generation` | [references/code-generation.md](./references/code-generation.md) |
| 任务拆解与执行 | `task-decomposition-and-execution` | [references/task-decomposition-and-execution.md](./references/task-decomposition-and-execution.md) |
| 技术选型 | `tech-selection` | [references/tech-selection.md](./references/tech-selection.md) |
| 文档生成 | `doc-generation` | [references/doc-generation.md](./references/doc-generation.md) |
| 测试用例生成 | `test-generation` | [references/test-generation.md](./references/test-generation.md) |
| 重构建议 | `refactoring` | [references/refactoring.md](./references/refactoring.md) |
| 项目记忆管理 | `project-memory-management` | [references/project-memory-management.md](./references/project-memory-management.md) |
## 跨技能协同指引

编程专家为独立技能套件，暂无可直接联动的其他职业技能。如需在编程任务中集成外部数据或服务，可使用主Agent的web_search/web_fetch工具获取。

## 变更日志

### v1.0.1 (2026-06-19)
- 对齐 description 子技能名与路由表名称
- 压缩路由表说明列至40字以内
- 新增跨技能协同指引章节
- 删除冗余英文 description 行