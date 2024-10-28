import streamlit as st
import requests
import openai

# Function to load API keys and URLs from config.txt
def load_config(file_path="config.txt"):
    config = {}
    with open(file_path, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key] = value
    return config

# Load API keys and URLs
config = load_config()
openai_api_key = config.get("OPENAI_API_KEY")
jira_email = config.get("JIRA_EMAIL")
jira_api_token = config.get("JIRA_API_TOKEN")
jira_url = config.get("JIRA_URL")
gitlab_url = config.get("GITLAB_URL")
gitlab_token = config.get("GITLAB_TOKEN")

# Check that all credentials are provided
if not openai_api_key or not jira_email or not jira_api_token or not jira_url or not gitlab_token:
    st.error("Please ensure all API keys and URLs are provided in config.txt.")
else:
    openai.api_key = openai_api_key
    st.title("Developer Assistant Chatbot")
    st.write("A tool to streamline daily tasks and support developers using GitLab and Jira.")

    # 1. Automated Issue Assignment and Updates
    st.subheader("Assign Issue")
    issue_key = st.text_input("Enter Issue Key for Assignment")
    assignee = st.text_input("Enter Assignee Username")
    if st.button("Assign Issue"):
        def assign_issue(issue_key, assignee):
            auth = (jira_email, jira_api_token)
            url = f"{jira_url}/rest/api/2/issue/{issue_key}/assignee"
            data = {"name": assignee}
            response = requests.put(url, json=data, auth=auth)
            if response.status_code == 204:
                st.write(f"Issue {issue_key} has been assigned to {assignee}.")
            else:
                st.write(f"Failed to assign issue: {response.text}")
        assign_issue(issue_key, assignee)

    # 2. Sprint and Project Management Insights
    st.subheader("Sprint Progress")
    project_key = st.text_input("Enter Project Key for Sprint Insights")
    if st.button("Get Sprint Progress"):
        def get_sprint_progress(project_key):
            auth = (jira_email, jira_api_token)
            jql = f"project = {project_key} AND sprint in openSprints()"
            response = requests.get(f"{jira_url}/rest/api/2/search?jql={jql}", auth=auth)
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                for issue in issues:
                    st.write(f"Issue: {issue['key']}, Status: {issue['fields']['status']['name']}")
            else:
                st.write("Failed to retrieve sprint progress.")
        get_sprint_progress(project_key)

    # 3. Automated Daily Standup Summary
    st.subheader("Daily Standup Summary")
    if st.button("Generate Standup Summary"):
        def daily_standup_summary():
            auth = (jira_email, jira_api_token)
            jql = "status != Done ORDER BY assignee"
            response = requests.get(f"{jira_url}/rest/api/2/search?jql={jql}", auth=auth)
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                summary = {}
                for issue in issues:
                    assignee = issue["fields"]["assignee"]["displayName"]
                    summary.setdefault(assignee, []).append(issue["key"])
                for person, tasks in summary.items():
                    st.write(f"{person} is working on issues: {', '.join(tasks)}")
            else:
                st.write("Failed to retrieve daily standup summary.")
        daily_standup_summary()

    # 4. Priority-Based Task List for Developers
    st.subheader("Priority Task List")
    assignee = st.text_input("Enter Assignee for Priority Tasks")
    priority = st.selectbox("Select Priority", ["High", "Medium", "Low"])
    if st.button("Get Priority Tasks"):
        def get_priority_tasks(assignee, priority):
            auth = (jira_email, jira_api_token)
            jql = f"assignee = {assignee} AND priority = {priority}"
            response = requests.get(f"{jira_url}/rest/api/2/search?jql={jql}", auth=auth)
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                for issue in issues:
                    st.write(f"Issue: {issue['key']}, Summary: {issue['fields']['summary']}")
            else:
                st.write("Failed to retrieve priority tasks.")
        get_priority_tasks(assignee, priority)

    # 5. Automated Notifications for Blocked Tasks
    st.subheader("Check Blocked Tasks")
    if st.button("Check Blocked Tasks"):
        def check_blocked_tasks():
            auth = (jira_email, jira_api_token)
            jql = "status = Blocked"
            response = requests.get(f"{jira_url}/rest/api/2/search?jql={jql}", auth=auth)
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                for issue in issues:
                    st.write(f"Blocked Issue: {issue['key']} - {issue['fields']['summary']}")
            else:
                st.write("Failed to check blocked tasks.")
        check_blocked_tasks()

    # 6. GitLab Deployment Tracking
    st.subheader("GitLab Deployment Status")
    project_id = st.text_input("Enter GitLab Project ID for Deployment Status")
    if st.button("Check Deployment Status"):
        def track_gitlab_deployment_status(project_id):
            headers = {"PRIVATE-TOKEN": gitlab_token}
            url = f"{gitlab_url}/api/v4/projects/{project_id}/deployments"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                deployments = response.json()
                for deployment in deployments:
                    st.write(f"Deployment ID: {deployment['id']}, Status: {deployment['status']}, Created at: {deployment['created_at']}")
            else:
                st.write("Failed to fetch deployment data.")
        track_gitlab_deployment_status(project_id)

    # 7. Generate Progress Reports and Metrics
    st.subheader("Generate Project Report")
    project_key = st.text_input("Enter Project Key for Report")
    if st.button("Generate Report"):
        def generate_progress_report(project_key):
            auth = (jira_email, jira_api_token)
            jql = f"project = {project_key}"
            response = requests.get(f"{jira_url}/rest/api/2/search?jql={jql}", auth=auth)
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                report = {issue['key']: issue['fields']['status']['name'] for issue in issues}
                st.write(report)
            else:
                st.write("Failed to generate report.")
        generate_progress_report(project_key)

    # 8. Knowledge Base Integration for Developer Support
    st.subheader("Search Knowledge Base")
    query = st.text_input("Enter your query for the Knowledge Base")
    if st.button("Search Knowledge Base"):
        def search_knowledge_base(query):
            response = requests.get(f"{confluence_url}/search?query={query}", auth=(jira_email, jira_api_token))
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.write("Failed to retrieve knowledge base data.")
        search_knowledge_base(query)

    # 9. GitLab Code Review Reminders
    st.subheader("Pending GitLab Merge Requests")
    assignee_username = st.text_input("Enter Assignee Username for Merge Requests")
    if st.button("Check Pending Merge Requests"):
        def check_pending_merge_requests(assignee_username):
            headers = {"PRIVATE-TOKEN": gitlab_token}
            url = f"{gitlab_url}/api/v4/merge_requests?scope=all&state=opened&reviewer_username={assignee_username}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                merge_requests = response.json()
                for mr in merge_requests:
                    st.write(f"Merge Request ID: {mr['id']}, Title: {mr['title']}, Created at: {mr['created_at']}")
            else:
                st.write("Failed to fetch merge requests.")
        check_pending_merge_requests(assignee_username)

    # 10. Monitor Project Health and Alert on Issues
    st.subheader("Monitor Project Health")
    project_key = st.text_input("Enter Project Key for Health Check")
    if st.button("Monitor Project Health"):
        def monitor_project_health(project_key):
            auth = (jira_email, jira_api_token)
            jql = f"project = {project_key} AND priority = High"
            response = requests.get(f"{jira_url}/rest/api/2/search?jql={jql}", auth=auth)
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                if issues:
                    st.write(f"High-priority issues found in project {project_key}.")
                else:
                    st.write(f"No high-priority issues in project {project_key}.")
            else:
                st.write("Failed to monitor project health.")
        monitor_project_health(project_key)
