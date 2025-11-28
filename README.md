# 学生福祉监测系统 (Student Wellbeing Monitoring System)

本项目是一个用于整合、分析和可视化学生的学习参与度与福祉数据的原型系统。它包含一个 Vue.js 前端和一个 Flask 后端。

## 技术栈

*   **后端**: Python, Flask, SQLAlchemy
*   **前端**: Vue 3, TypeScript, Vite, Pinia, Axios
*   **数据库**: SQLite (用于开发和测试)
*   **测试**: Pytest (后端), Vitest (前端)

## 环境准备


*   Python (推荐版本 3.9+)
*   Node.js (推荐版本 18+)

## 项目结构

本项目采用前后端分离的架构：

*   **`app/`**: Flask 后端的核心业务逻辑模块，包含认证、管理、警报、分析、模型和仓库等。
*   **`frontend/vue-project/`**: Vue.js 前端应用程序的根目录，包含所有前端源代码和配置。
*   **`app.py`**: Flask 后端应用程序的入口文件。
*   **`config.py`**: 后端配置管理。
*   **`tests/`**: 项目的测试文件。
*   **`.venv/`**: Python 虚拟环境目录。

## 主要功能

### 后端 (Flask)

*   **用户认证与授权**: 提供用户注册、登录、登出及权限管理。
*   **管理功能**: 后台用户及系统配置管理。
*   **数据模型与存储**: 定义数据结构，提供数据库交互接口。
*   **警报/通知系统**: 创建、管理和发送各类警报。
*   **数据分析**: 处理并提供数据分析接口。

### 前端 (Vue.js)

*   **用户界面**: 展示后端数据，提供直观的用户操作界面。
*   **用户交互**: 处理用户输入，响应用户操作，与后端 API 交互。
*   **页面与路由**: 管理前端页面导航和视图展示。

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

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 2. 安装后端依赖
pip install -r requirements.txt

# 3. (可选) 创建 .flaskenv 文件并设置环境变量
# 在项目根目录创建一个名为 .flaskenv 的文件，并填入以下内容：
# FLASK_CONFIG=development # 或 'default'
```

### 3. 前端设置

```bash
# 1. 进入前端项目目录
cd frontend/vue-project

# 2. 安装前端依赖
npm install

# 3. (可选) 配置 API 代理
# 为了在开发时解决跨域问题，请确保 vite.config.ts 中有类似以下的代理设置：
# server: {
#   proxy: {
#     '/api': {
#       target: 'http://127.0.0.1:5000', // 你的 Flask 后端地址
#       changeOrigin: true,
#     }
#   }
# }
```

## 运行项目

你需要同时运行前端和后端开发服务器。

1.  **运行后端服务**:
    *   确保你的 Python 虚拟环境已激活。
    *   在项目根目录运行：
        ```bash
        python app.py
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
    pytest
    ```

*   **前端测试**:
    ```bash
    # 进入 frontend/vue-project 目录
    npm test
    ```