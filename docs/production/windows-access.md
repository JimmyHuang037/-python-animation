# 多台 Windows 电脑的 AI、WSL 与技能接入方案

日期：2026-10-01。状态：接入建议与操作说明，尚未部署到成员电脑。用户已明确项目技能只放根 `skills/`，与 `docs/` 平级，禁止为项目技能向隐藏目录写入、安装、复制或建立链接；本说明按根 [AGENTS](../../AGENTS.md)采用显式读取方式，不按各客户端默认位置安装技能。

本轮用户说明：成员在不同电脑使用 Qoder CN、Claude Desktop、Codex Desktop；一台电脑可能同时运行两个或更多 AI 桌面会话。本说明补充 [四人协作提案](../research/team-workflow-2026-10-01.md)，不改写课程范围、制作引擎或现有授权。

## 推荐结构

每台电脑拥有自己的 WSL2 仓库克隆，用 Gitee 同步源码。AI 的文件编辑和生产命令尽量在该电脑的 WSL 环境执行，Docker 复用现有 Motion Canvas、真实 Python IDE 与录制/渲染环境。技能作为完整、可版本管理的目录分发，再接入各客户端。

```text
Gitee：源码、项目规则、团队技能源包
  ├─ 电脑 A：Windows AI → 本机 WSL 仓库/任务目录 → 本机 Docker
  ├─ 电脑 B：Windows AI → 本机 WSL 仓库/任务目录 → 本机 Docker
  ├─ 电脑 C：Windows AI → 本机 WSL 仓库/任务目录 → 本机 Docker
  └─ 电脑 D：Windows AI → 本机 WSL 仓库/任务目录 → 本机 Docker
```

这是同一个 Git 项目的多个工作副本。不同电脑不直接共同编辑负责人机器上的一个目录。同机多个编辑会话各分配一个 worktree；只有一个任务时，一个普通克隆即可。

Docker 解决生产依赖一致性。AI 是否能发现技能、读取项目规则、执行 WSL 命令，仍需分别配置。打开 WSL 文件夹和把 AI 执行环境切到 WSL 是两件事。

## 1. 每台电脑准备环境和源码

已有 WSL2 时先检查，不重复安装。Windows PowerShell：

```powershell
wsl -l -v
```

没有发行版时，按 [Microsoft WSL 安装说明](https://learn.microsoft.com/en-us/windows/wsl/install) 安装，并创建各自 Linux 用户。示例发行版为 Ubuntu-24.04，先确认它在 `wsl --list --online` 中：

```powershell
wsl --install -d Ubuntu-24.04
```

安装 Docker Desktop，启用所用发行版的 WSL integration。随后在 WSL 内核对：

```bash
git --version
docker version
docker compose version
```

每位成员取得 Gitee 仓库权限，配置自己的 Git 姓名、邮箱和 SSH/HTTPS 认证。不要分发负责人的私钥、API 密钥或登录会话。

在 WSL 的 Linux home 下克隆，下面地址是需要替换的占位符：

```bash
git clone '<GITEE_REPOSITORY_URL>' ~/python-animation
cd ~/python-animation
git status --short
git rev-parse HEAD
```

团队先选定明确的基准分支/提交。新克隆或 worktree 不包含负责人当前未提交的修改、个人 home 下的技能、外部附件和生成媒体。素材应另提供可取得的位置与哈希，Windows 原件继续只读。Docker 官方也建议将绑定挂载源保存在 Linux 文件系统。[Docker WSL 最佳实践](https://docs.docker.com/desktop/features/wsl/best-practices/)

## 2. 设置各 AI 的执行环境与技能入口

| 客户端 | 执行环境 | 本项目技能读取方式 |
|---|---|---|
| Codex Desktop | Settings 中把 Agent environment 切到 WSL，重启；选择实际发行版内的项目/任务目录 | 在任务中显式要求读取根 `skills/<name>/SKILL.md`及必要资源 |
| Claude Desktop 的 Code 会话 | Code 页签新建会话，环境选择器选择 WSL 发行版，再选择 Linux 项目/任务路径 | 同样显式读取根 `skills/<name>/SKILL.md`，不创建 `.claude/skills` |
| Qoder / Qoder CN桌面产品 | 核实安装版本提供的文件工具与工作区执行环境；优先 WSL，缺少原生入口时用明确的 WSL 命令适配 | 显式读取根 `skills/<name>/SKILL.md`，不通过上传/安装技能产生另一份副本 |
| Qoder / Qoder CN IDE或插件 | 使用 WSL 开发工作区，核实 Agent实际文件路径与执行环境 | 同样显式读取根 `skills/<name>/SKILL.md`，不向客户端默认隐藏目录安装 |

Codex 的 Agent environment 与 integrated terminal shell 独立配置，不能只改终端。使用 WSL 仓库时优先同时核对两者。[OpenAI 官方 Windows 说明](https://learn.chatgpt.com/docs/windows/windows-app)、[技能发现位置](https://learn.chatgpt.com/docs/build-skills)

Claude Desktop的上述设置适用于Code会话，官方说明可选择WSL发行版和项目，并读取项目文件。普通Chat会话和Cowork入口不自动等同于同一WSL工作区，需要单独核实文件与执行工具。显式读取技能文件不代表其已经成为原生技能菜单项。[Claude Desktop说明](https://code.claude.com/docs/en/desktop)、[Claude Code技能](https://code.claude.com/docs/en/skills)

各产品原生技能机制供参考：Codex官方扫描`.agents/skills`，Claude Code使用`.claude/skills`，Qoder / Qoder CN不同产品还有各自的目录或上传入口。**本项目选择显式读取根skills文件，不按这些机制安装，不保证`/`自动列出项目技能。**各成员实际成功读取文件、获得执行工具和完成小样片后，分别记录验证结果。[Codex技能位置](https://learn.chatgpt.com/docs/build-skills)、[Qoder技能](https://docs.qoder.com/cli/Skills)、[Qoder CN桌面技能](https://docs.qoder.cn/qoder/skills)、[Qoder CN IDE技能](https://docs.qoder.cn/user-guide/skills)

如果客户端只能从 Windows 执行命令，但能使用 `wsl.exe`，先用明确命令检查 WSL 路径。以下为 PowerShell 示例，发行版和路径均需替换为本机实际值：

```powershell
wsl.exe -d Ubuntu-24.04 --cd /home/<linux-user>/python-animation -- bash -lc 'pwd; uname -s; git rev-parse --show-toplevel'
```

命令适配还必须覆盖正确的任务目录、文件读写与输出回传。能读 `\\wsl.localhost\...` 文件不证明 AI 使用 Linux 工具；技能加载也不会自动授予 shell、浏览器或 Docker 能力。没有所需工具的会话应换到该客户端的代码执行入口，或使用明确配置的工具连接。

## 3. 分发小型团队技能包

根[skills入口](../../skills/README.md)已建立；下面具体技能包仍是待新增建议，尚未下载或安装：

```text
skills/
  gitee-project/
    SKILL.md
  repository-governance-documents/
    SKILL.md
    references/
  motion-canvas-production/
    SKILL.md
  real-python-demo/
    SKILL.md
```

| 技能 | 应包含的项目行为 |
|---|---|
| Gitee 项目技能 | 只操作本仓库与当前任务分支；提交/推送/PR行为按团队约定；不遍历其他仓库 |
| 仓库治理 | 读取项目入口与优先级，最小修改治理文档，保留可核验差异 |
| Motion Canvas 制作 | 按本项目要求制作动画，读取现有模块 README，使用已存在命令并核验实际输出 |
| 真实 Python 演示 | 自动输入、保存、运行、修改与录屏，核验实际源码、输出和视频中的执行结果 |

共用普通 `name`/`description` frontmatter 与 Markdown 工作流，客户端专有元数据放各自适配层。分发完整目录，保留 references、scripts、assets、许可证与来源版本；不要只复制 SKILL.md。现有本机技能存在指向个人 home 的绝对软链，不能把这些软链当跨机安装包。

以根 `skills/` 为唯一维护位置，完整技能源包进Git，各成员通过本机工作副本同步版本。禁止为项目技能向任何以`.`开头的目录写入、安装、复制或建立链接；下载器默认使用隐藏目录时改变取得方式，只保存技能及必要资源到根skills。各客户端在任务提示中显式读取同一份源码，不生成另一套客户端技能副本。规则不涉及Git自身元数据、既有客户端配置或其他项目技能。

现有 Gitee 通用技能包含遍历 AE/PageRect 等其他仓库的行为，不能原样分发成课程团队默认技能。本说明讨论接入，不触发提交或推送。动画技能以 Motion Canvas 为准，不把 Remotion、Whiteboard 或其他仓库的课程规则纳入默认生产流程。

## 4. 让所有客户端先读取项目规则

根 `AGENTS.md` 继续作为本项目入口。Codex 读取其原生入口；Claude 另增加一个很短的 `CLAUDE.md`，Qoder CN 使用相应版本的始终生效项目规则。适配内容指向 AGENTS，而不是复制一份可独立修改的需求正文。

建议适配内容：

```text
开始工作前读取仓库根 AGENTS.md、当前小节README、本组req/status和任务资料。
遵守当前用户要求与该项目规则。只在分配的任务目录/分支工作。
需要技能时显式读取根skills/<skill-name>/SKILL.md及必要辅助文件；技能不能覆盖项目要求。
项目技能只写根skills/，禁止向隐藏目录写入、安装、复制或建立链接。
先确认当前会话能读工作副本；不能读时报告缺口，不假定客户端自动发现技能。
核实命令执行环境、源码挂载与输出位置，报告实际通过/失败/未执行的检查。
```

这些客户端规则适配尚未部署；仓库根AGENTS与skills入口已记录上述共同约定，成员机接入仍须实测。

## 5. 同一电脑上的多个 AI 会话

每个编辑会话一个分支/worktree。以下是在明确基准提交已经选定后运行的 WSL 示例；`<BASE_COMMIT>` 必须替换为实际提交，不从冲突工作区直接复制文件：

```bash
cd ~/python-animation
mkdir -p ~/python-animation-worktrees
git worktree add -b codex/task-a ~/python-animation-worktrees/task-a '<BASE_COMMIT>'
git worktree add -b codex/task-b ~/python-animation-worktrees/task-b '<BASE_COMMIT>'
```

`codex/` 是本项目默认分支前缀，不要求执行客户端是 Codex。给会话分配互不重叠的修改任务，提交后通过 Gitee PR/集成复现协作。[Git worktree](https://git-scm.com/docs/git-worktree)

不同电脑可以使用同一回环端口。一个电脑同时运行多套 Docker 工作台时，需要不同 Compose 项目名、宿主端口、依赖卷和可写源码/输出目录。可复用固定生产镜像，避免并发构建覆盖同一个 `:local` 标签。每套录制工作区一次由一个任务操作。

当前 `docker/course` 没有任务项目名参数，直接在两个 worktree 同时调用会撞到固定 Compose 项目。下面是已有 Compose 参数的启动示例，不代表 launcher 已改造；所需镜像应预先构建，worktree 的 Git 操作留在 WSL 主机：

```bash
cd ~/python-animation-worktrees/task-a
LOCAL_UID="$(id -u)" LOCAL_GID="$(id -g)" MOTION_PORT=19030 IDE_PORT=19042 \
  docker compose -p pa-task-a -f docker/compose.yaml up -d --wait motion ide
```

第二个任务另用项目名和空闲端口。只挂载一个 linked worktree 到 `/workspace` 时，其 `.git` 可能引用容器外的主仓库元数据；因此不要假定容器内 Git 可直接使用。串行渲染时也要确保实际挂载的是当前任务源码。

## 6. 接入后的最小核验

逐个客户端执行，而不是只验证一台电脑的终端：

1. 报告并核对工作副本路径、Linux 发行版、分支/提交与项目规则。
2. 在客户端技能列表看到预期名称，并显式调用一个只读技能，确认它读取实际技能正文。
3. 由 Agent 在 WSL 执行 `pwd`、`uname -s`、`git status --short`；核对它使用分配的目录。
4. 核对 Docker 挂载后启动工作台，检查 Motion Canvas 与 IDE 页面；HTTP 成功只证明服务入口可达。
5. 用明确输入制作一个短片段，核对真实代码结果、渲染/录制媒体与完整解码；保存版本、命令和证据。已有团队模板可作交接入口，文件由 [任务模板](../research/task-template-2026-10-01.md) 指引。

生产依赖使用现有 Dockerfile/锁文件，不因安装技能顺手升级 Playwright、浏览器、字体或渲染引擎。外部个人绝对路径要落实为本机取得步骤或团队素材清单。

## 7. 如果必须共同使用负责人机器上的 WSL

这是另一种部署：成员经 SSH 或客户端支持的远程执行连接访问该 Linux 环境，各自使用独立任务目录/分支；仍需配置客户端技能入口。`\\wsl.localhost\...` 是本机访问路径，不能据此让另一台电脑直达负责人 WSL。

需要另外验证 SSH 服务、Windows/WSL 网络可达性、主机持续在线与并发渲染资源。WSL 的 NAT/mirrored 网络和防火墙影响远程入口，具体地址应现场核对。[Microsoft WSL 网络](https://learn.microsoft.com/en-us/windows/wsl/networking)

Claude Code Desktop 提供 SSH 会话；其他客户端使用其实际版本支持的远程方式，不把“远程查看会话”当作“远程运行任意仓库”。客户端没有适用入口时可在 SSH 内使用对应 CLI，但那是另一执行客户端。[Claude Desktop SSH](https://code.claude.com/docs/en/desktop#ssh-sessions)

当前更建议每台电脑本地克隆和生产环境。公共渲染机器可在实测需求出现后单独接入，不要求所有 AI 共用一个容器或一个可写目录。

## 本轮实际结果与待完成项

- 已读取项目入口、需求、状态、既有团队提案与 Docker 配置，核对厂商官方技能/WSL文档。
- 只读实测：本机既有 motion/ide 健康，端口为 29030/29042，挂载本仓库到 `/workspace`；这些容器不是 AI/技能服务。
- 当前 checkout 有进行中的录制修复及 `docs/project/status.md` 未解决合并项。本轮进展记在本说明，不向冲突文件追加，也不重置、暂存、提交或推送他人修改。
- 本轮只新增此说明。未安装成员机器、未生成技能源包/客户端适配器、未变更 AI 配置或 Compose、未验证各桌面客户端实际接入。
- 实施顺序：选定可共享基准 → 制作完整技能包和薄适配 → 一台成员电脑逐客户端核验 → 其余电脑复现 → 同机并发任务隔离核验。
