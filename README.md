# 学生福祉监测系统 (Student Wellbeing Monitoring System)

本项目是一个用于整合、分析和可视化学生的学习参与度与福祉数据的原型系统。它包含一个 Vue.js 前端和一个 Flask 后端，旨在帮助教育机构更好地理解和支持学生的整体健康与学业表现。

## 技术栈

*   **后端**: Python, Flask, Flask-JWT-Extended, SQLite (直接操作 `sqlite3` 模块), Werkzeug, python-dotenv
*   **前端**: Vue 3, TypeScript, Vite, Pinia, Axios
*   **数据库**: SQLite (用于开发和测试环境，数据文件为 `data-dev.sqlite` / `data-test.sqlite`)
*   **测试**: Pytest (后端), Vitest (前端单元测试), Playwright (前端 E2E 测试)

## 环境准备

*   **Python**: 推荐版本 3.9+
*   **Node.js**: 推荐版本 18+ (用于前端开发)

## 项目结构

本项目采用前后端分离的架构，主要目录和文件说明如下：

*   **`app/`**: Flask 后端的核心业务逻辑模块，包含：
    *   `auth/`: 用户认证与授权相关逻辑。
    *   `admin/`: 管理员功能（CRUD 操作）。
    *   `analysis/`: 数据分析接口。
    *   `student/`: 学生相关接口。
    *   `models/`: 数据库模型定义。
    *   `repositories/`: 数据库交互层（Repository 模式）。
    *   `db_connection.py`: 数据库连接管理。
    *   `utils/`: 应用内部工具函数（如权限装饰器）。
*   **`frontend/vue-project/`**: Vue.js 前端应用程序的根目录，包含所有前端源代码和配置。
*   **`app.py`**: Flask 后端应用程序的入口文件，用于创建 Flask 应用实例。
*   **`config.py`**: 后端配置管理（开发、测试、生产环境）。
*   **`manage.py`**: 后端管理脚本，包含数据库初始化、数据填充等 CLI 命令。
*   **`tests/`**: 后端 Pytest 测试文件。
*   **`utils/`**: 项目通用工具函数（如数据填充脚本 `seed_data.py`）。
*   **`.venv/`**: Python 虚拟环境目录 (由 `python -m venv` 创建)。
*   **`requirements.txt`**: 后端 Python 依赖列表。
*   **`package.json`**: 前端 Node.js 依赖列表。
*   **`data-dev.sqlite` / `data-test.sqlite`**: 开发/测试环境的 SQLite 数据库文件。

## 主要功能

### 后端 (Flask API)

*   **用户认证与授权**: 基于 JWT (JSON Web Tokens) 的用户注册、登录、登出及基于角色的权限管理 (`admin`, `course_director`, `wellbeing_officer`, `student`)。
*   **数据管理 (CRUD)**: 为学生、模块、用户、选课、成绩、考勤记录、提交记录、调查问卷、压力事件和警报提供完整的 CRUD API。
*   **数据分析**: 提供仪表盘摘要、成绩分布、压力-成绩关联、整体出勤率、提交状态分布、高风险学生识别等分析接口。
*   **警报/通知系统**: 管理和解析学生福祉警报。

### 前端 (Vue.js 应用)

*   **直观的用户界面**: 展示后端数据，提供友好的用户操作界面。
*   **数据可视化**: 可能包含图表和图形，用于展示分析数据。
*   **用户交互**: 处理用户输入，响应用户操作，通过 Axios 与后端 API 交互。
*   **状态管理**: 使用 Pinia 进行应用状态管理。
*   **路由管理**: 使用 Vue Router 进行页面导航和视图展示。

## 本地开发环境搭建

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd group-assessment-v3 # 根据你的实际项目目录名调整
```

### 2. 后端设置

```bash
# 1. 创建并激活 Python 虚拟环境
# 如果 .venv 目录已存在，则直接激活
python3 -m venv .venv

# Windows PowerShell
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 2. 安装后端依赖
pip install -r requirements.txt

# 3. 初始化数据库 (创建表并填充初始数据)
# 这一步会删除旧的数据库文件（如果存在）并创建新的表结构，然后填充初始数据。
# 请确保在项目根目录执行，且虚拟环境已激活。

# 首先，设置 FLASK_APP 环境变量指向 manage.py
# Windows PowerShell
$env:FLASK_APP="manage.py"
# macOS / Linux
export FLASK_APP=manage.py

# 运行数据库初始化命令
# 这将删除 data-dev.sqlite (如果存在)，并根据 seed_data.py 重新创建和填充数据。
flask init-db 
```

### 3. 前端设置

```bash
# 1. 进入前端项目目录
cd frontend/vue-project

# 2. 安装前端依赖
npm install

# 3. (可选但推荐) 配置 API 代理
# 为了在开发时解决跨域问题，请确保 frontend/vue-project/vite.config.ts 中有类似以下的代理设置：
# server: {
#   proxy: {
#     '/api': {
#       target: 'http://127.0.0.1:5000', # 你的 Flask 后端地址
#       changeOrigin: true,
#       rewrite: (path) => path.replace(/^\/api/, '/api'), // 确保路径重写正确
#     }
#   }
# }
```

## 运行项目

你需要同时运行前端和后端开发服务器。请打开两个独立的终端窗口。

1.  **运行后端服务**:
    *   确保你的 Python 虚拟环境已激活。
    *   在项目根目录运行：
        ```bash
        # 首先，设置 FLASK_APP 环境变量指向 manage.py (如果之前未设置)
        # Windows PowerShell
        $env:FLASK_APP="manage.py"
        # macOS / Linux
        export FLASK_APP=manage.py

        # 运行 Flask 应用 (使用 manage.py 的 run 命令)
        python manage.py run
        ```
    *   后端服务将默认在 `http://127.0.0.1:5000` 启动。

2.  **运行前端服务**:
    *   打开一个新的终端。
    *   进入 `frontend/vue-project` 目录。
    *   运行：
        ```bash
        npm run dev
        ```
    *   前端开发服务器将启动，你可以在浏览器中打开提示的地址（通常是 `http://localhost:5173`）。

## 运行测试

*   **后端测试**:
    ```bash
    # 在项目根目录，确保虚拟环境已激活
    pytest --cov=app # 运行所有后端测试并生成覆盖率报告
    ```

*   **前端测试**:
    ```bash
    # 进入 frontend/vue-project 目录
    npm run test:unit # 运行单元测试
    npm run test:e2e # 运行端到端测试
    ```

## 清理本地环境 (可选)

你可以安全地删除以下自动生成的文件和目录，它们不会影响项目功能：

*   `__pycache__/` (所有子目录)
*   `.pytest_cache/`
*   `data-dev.sqlite` / `data-test.sqlite` (如果你可以通过 `flask init-db` 重新生成数据库)
*   `node_modules/` (前端依赖，可以通过 `npm install` 重新生成)
*   `.venv/` (Python 虚拟环境，可以通过 `python3 -m venv .venv` 重新生成)
*   `.idea/` (IDE 配置文件)
