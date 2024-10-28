import streamlit as st
import requests
import openai

# Function to load API keys and URLs from config.txt
def load_config(file_path="config.txt"):
    config = {}
    with open(file_path, "r") as f:
        for line in f:
            # Ignore empty lines or lines without an "=" character
            if "=" in line:
                key, value = line.strip().split("=", 1)  # Split only on the first "="
                config[key] = value
    return config

# Load API keys and URLs
config = load_config()
openai_api_key = config.get("OPENAI_API_KEY")
jira_email = config.get("JIRA_EMAIL")
jira_api_token = config.get("JIRA_API_TOKEN")
jira_url = config.get("JIRA_URL")

# Check that all credentials are provided.
if not openai_api_key or not jira_email or not jira_api_token or not jira_url:
    st.error("Please ensure all API keys and URLs are provided in config.txt.")
else:
    # Set OpenAI API key
    openai.api_key = openai_api_key

    # Show title and description.
    st.title("💬 Developer Assistant Chatbot")
    st.write(
        "This chatbot uses OpenAI's GPT-4.0 model alongside data from Jira to provide insights on ongoing projects."
    )

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to retrieve and parse data from Jira
    def search_jira(query):
        auth = (jira_email, jira_api_token)  # Use Basic Authentication with email and API token
        params = {"jql": query}  # JQL query to filter issues
        response = requests.get(f"{jira_url}/rest/api/2/search", auth=auth, params=params)
        
        if response.status_code == 200:
            return parse_jira_response(response.json())
        else:
            st.error(f"Failed to fetch data from Jira: {response.status_code}")
            st.write(response.text)  # Output error response text for further inspection
            return []

    # Function to parse Jira response for human-readable format
    def parse_jira_response(response_json):
        issues = response_json.get("issues", [])
        parsed_issues = []

        for issue in issues:
            fields = issue.get("fields", {})
            parsed_issue = {
                "ID": issue.get("id"),
                "Key": issue.get("key"),
                "Summary": fields.get("summary", "N/A"),
                "Description": fields.get("description", "N/A"),
                "Assignee": fields.get("assignee", {}).get("displayName", "Unassigned") if fields.get("assignee") else "Unassigned",
                "Status": fields.get("status", {}).get("name", "Unknown"),
                "Project Name": fields.get("project", {}).get("name", "Unknown")
            }
            parsed_issues.append(parsed_issue)

        return parsed_issues

    # Function to generate a human-like response from GPT-4 based on parsed Jira data
    def generate_response_from_model(user_query, parsed_issues):
        # Create a natural language summary of the issues
        issues_text = "\n\n".join(
            f"Issue {issue['Key']}: {issue['Summary']} - Status: {issue['Status']} - "
            f"Assigned to: {issue['Assignee']}" for issue in parsed_issues
        )

        # Construct the prompt for GPT-4
        prompt = (
            f"You are an assistant that helps analyze Jira data for security projects. Based on the following data, "
            f"answer the question in a helpful and conversational tone.\n\n"
            f"Jira Data:\n{issues_text}\n\n"
            f"User question: {user_query}"
        )

        # Call the OpenAI API to get the response
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for answering Jira-related questions."},
                {"role": "user", "content": prompt}
            ]
        ).choices[0].message['content']

        return response

    # Streamlit interface for the chatbot
    user_query = st.text_input("Ask a question about your Jira projects:")

    if user_query:
        # Retrieve and parse Jira data
        parsed_issues = search_jira("status != 'Done'")  # Fetch open issues
        if parsed_issues:
            # Generate response from the language model
            response = generate_response_from_model(user_query, parsed_issues)
            st.write(response)
        else:
            st.write("No relevant data found in Jira.")
