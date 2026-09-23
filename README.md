# Git Autopilot

Git Autopilot is an AI-powered tool that bridges your GitHub repository with local development environments. It automates the workflow by analyzing GitHub Issues, processing them with AI, and executing the necessary coding tasks in your local workspace.

This repository contains multiple directories, each tailored for specific development environments (e.g., ESP32, ESP8266).

## 📂 Repository Structure

The project is organized by hardware/development platform. Each folder contains the necessary configurations and Docker setups for that specific target.

| Directory | Description | Status |
| :--- | :--- | :--- |
| `esp32/` | Configuration and tooling for ESP32 development | ✅ Active |
| `esp8266/` | Configuration and tooling for ESP8266 development | ✅ Active |
| `...` | *(More platforms coming soon)* | 🚧 Planned |

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:

*   **GitHub Account**
*   **Git**
*   **Docker** and **Docker Compose**
*   A browser

## 🚀 Installation & Setup

### 1. Configure GitHub Personal Access Token (PAT)

The tool requires a GitHub token to interact with your repositories.

1.  Go to your [GitHub Settings](https://github.com/settings/profile).
2.  Navigate to **Developer Settings** → **Personal access tokens** → **Tokens (Classic)**.
3.  Click **Generate new token (Classic)**.
4.  **Expiration**: Select a longer term (e.g., 90 days or "No expiration" if allowed).
5.  **Select scopes**: **Check all boxes** to ensure the tool has full permission to manage repos, issues, and workflows.
6.  Click **Generate token**.
7.  **Copy and save the token** securely. You will need this in the next step.

### 2. Clone and Launch the Environment

Navigate to your desired workspace directory and launch the specific environment for your target hardware.

```bash
# Navigate to your workspace
cd /your/workspace

# Clone the repository
git clone https://github.com/KodeSurge/git-autopilot.git

# Navigate into the specific hardware directory (Example: ESP32)
cd git-autopilot/esp32

# Start the Docker container in detached mode
docker compose up -d
```

*Note: Replace `esp32` with `esp8266` or other directories as needed.*

### 3. Initial Configuration (Web UI)

1.  Open your browser and navigate to:
    ```
    https://localhost:8081
    ```
    *(Note: If you encounter certificate errors, accept them or use `http://` if your setup allows it, but `https` is recommended for security.)*

2.  **Sign In**:
    *   Username: `admin`
    *   Password: `admin123`
    *   *(Follow any on-screen prompts to change your password or complete the initial setup.)*

3.  **Enable AI Service**:
    *   Go to **Billing**.
    *   Click **Enable AI Service**.

4.  **Initialize Repository**:
    *   Go to **Settings**.
    *   Navigate to **Init Repo**.
    *   Click **Refresh** to load your GitHub repositories.
    *   Select the repository you wish to work with.
    *   Click **Init**.

## 📝 Workflow: How to Use

Once initialized, you can drive your development by creating GitHub Issues.

### Step 1: Create a Task in GitHub

1.  Go to your selected GitHub Repository.
2.  Click on **Issues** → **New Issue**.
3.  **Title**: Use the prefix `[TASK]` followed by a short description.
    *   *Example:* `[TASK] Implement BLE connection handler`
4.  **Body**: Describe the task in detail. Include any specific requirements, expected behavior, or edge cases.
5.  **Save** the issue.

### Step 2: Trigger the AI

After saving the issue:

1.  **Add Label**: Assign the label `ai:autopilot` to the issue.
2.  **Monitor Status**:
    *   The task will appear in the **Task Monitor** within the Git Autopilot UI with status **AI Analysis**.
    *   The AI will analyze the issue and prepare a plan/implementation.

### Step 3: Execution

You have two options to proceed:

**Option A: Wait for Analysis (Recommended)**
1.  Wait until the **AI Analysis** is complete in the Task Monitor.
2.  Go back to GitHub and **Assign the task to yourself**.
3.  The task will reappear in the Task Monitor with status **Task Processing**. The tool will now begin executing the code changes.

**Option B: Immediate Execution**
1.  Immediately after assigning the `ai:autopilot` label, **Assign the task to yourself** in GitHub without waiting for the analysis to finish.
2.  The system will automatically handle the analysis and processing in sequence.

## 🔧 Troubleshooting

*   **Connection Issues**: Ensure Docker is running and the port `8081` is not blocked.
*   **Token Errors**: If you receive 401/403 errors, check that your Personal Access Token is valid and has the correct scopes.
*   **Task Not Showing**: Ensure the repo has been correctly **Init**'ed in the Settings tab and that the `ai:autopilot` label is exactly correct.

## 📄 License

[Add your license information here, e.g., MIT License]

***

### Key Improvements Made:
1.  **Structure**: Added a clear table for the folder structure, addressing your point about multiple folders.
2.  **Clarity**: Broken down the instructions into logical phases (Prereqs, Installation, Configuration, Workflow).
3.  **Formatting**: Used code blocks for commands and bold text for critical actions (like checking boxes in GitHub).
4.  **Safety**: Added a note about changing the default admin password.
5.  **Workflow Logic**: Clarified the "Option A" vs "Option B" for assigning the task, which can be confusing in the raw instructions.
