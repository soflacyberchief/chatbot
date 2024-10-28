
# Developer Assistant Chatbot

A powerful chatbot designed to streamline daily tasks and support developers by integrating with GitLab and Jira. This chatbot is built using Streamlit, OpenAI’s GPT-4, and REST API calls to Jira and GitLab to provide insights, automate tasks, and simplify project management for development teams.

---

## Features

### 1. **Automated Issue Assignment and Updates**
   - **Description**: Allows users to assign Jira issues to team members directly from the chatbot.
   - **Usage**: Enter the issue key and assignee username, and click "Assign Issue". The chatbot will update the assignment in Jira.

### 2. **Sprint and Project Management Insights**
   - **Description**: Provides insights on sprint progress, including issues in the current sprint and their statuses.
   - **Usage**: Enter the Jira project key, then click "Get Sprint Progress" to retrieve the status of issues in the active sprint.

### 3. **Automated Daily Standup Summary**
   - **Description**: Compiles a summary of what each team member is working on, based on Jira assignments.
   - **Usage**: Click "Generate Standup Summary" to get a breakdown of tasks assigned to each developer.

### 4. **Priority-Based Task List for Developers**
   - **Description**: Displays a list of high, medium, or low priority tasks for a specified developer.
   - **Usage**: Enter the assignee username and select the priority level, then click "Get Priority Tasks".

### 5. **Automated Notifications for Blocked Tasks**
   - **Description**: Notifies users of tasks that are currently blocked, helping them to identify issues that need attention.
   - **Usage**: Click "Check Blocked Tasks" to view all tasks with a status of "Blocked".

### 6. **GitLab Deployment Tracking**
   - **Description**: Tracks recent deployments for a specified GitLab project, providing deployment status and timestamps.
   - **Usage**: Enter the GitLab project ID and click "Check Deployment Status" to see recent deployment information.

### 7. **Generate Progress Reports and Metrics**
   - **Description**: Generates a report of open issues and their statuses for a specified Jira project.
   - **Usage**: Enter the Jira project key, then click "Generate Report" to receive an overview of project status.

### 8. **Knowledge Base Integration for Developer Support**
   - **Description**: Searches Confluence or other knowledge base sources to help answer questions.
   - **Usage**: Enter your query and click "Search Knowledge Base" to retrieve relevant documentation or resources.

### 9. **GitLab Code Review Reminders**
   - **Description**: Lists all open merge requests assigned to a specific GitLab user, helping developers keep track of pending code reviews.
   - **Usage**: Enter the assignee username and click "Check Pending Merge Requests" to see all open merge requests awaiting review.

### 10. **Monitor Project Health and Alert on Issues**
   - **Description**: Monitors Jira project health by tracking high-priority issues, providing an alert if any high-priority issues are open.
   - **Usage**: Enter the Jira project key and click "Monitor Project Health" to see if there are any high-priority issues.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/soflacyberchief/chatbot.git
   cd chatbot
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Configurations**:
   - Create a `config.txt` file (if it doesn’t already exist) in the root directory.
   - **Note**: Ensure `config.txt` is added to `.gitignore` to prevent accidental commits.

   Your `config.txt` should look like this, with environment variable placeholders (replace with actual values):
   ```plaintext
   OPENAI_API_KEY="YOUR_KEY_HERE"
   JIRA_EMAIL="YOUR_EMAIL_HERE"
   JIRA_API_TOKEN="YOUR_TOKEN_HERE"
   JIRA_URL="YOUR_JIRA_URL_HERE"
   GITLAB_URL="YOUR_GITLAB_URL_HERE"
   GITLAB_TOKEN="YOUR_GITLAB_TOKEN_HERE"
   ```

5. **Run the Application**:
   ```bash
   streamlit run streamlit_app_v3.py
   ```

   This will open the chatbot interface in your default web browser.

---

## Usage

### Interacting with the Chatbot

- **Assigning Issues**: Enter the Jira issue key and assignee username to assign the task directly.
- **Tracking Progress**: View sprint progress or generate daily standup summaries with a single click.
- **Monitoring Health**: Keep track of blocked tasks, high-priority issues, and deployments.
- **Knowledge Base Search**: Search documentation directly from the chatbot to get quick answers.

### Environment Variables

For security, all sensitive information (API keys and tokens) should be stored as environment variables in `config.txt` rather than hardcoding them.

### Example Commands

- **Assign an Issue**:
  - Enter the issue key and assignee to assign the issue to a developer.
- **View Sprint Progress**:
  - Enter the Jira project key to see all tasks in the current sprint.
- **Generate Standup Summary**:
  - Click the "Generate Standup Summary" button to get an overview of each team member’s current tasks.

---

## Troubleshooting

If you encounter issues when pushing to GitHub due to secrets in commit history:
1. **Clean Git History** with `git filter-repo` to remove sensitive data.
2. **Force push** the cleaned history:
   ```bash
   git push origin main --force
   ```
3. **Set environment variables locally** or in the CI/CD environment for security.

---

## Contributing

Feel free to contribute by creating pull requests, reporting issues, or suggesting features.

---

## License

This project is licensed under the MIT License.

---

### Important Links
- [GitHub Secret Scanning](https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line#resolving-a-blocked-push)

With this README, new users and developers should have a clear understanding of the project, how to set it up, and how to use each feature.
