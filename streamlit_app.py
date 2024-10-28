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
    st.title("💬 Travel and Leisure SecOps Chatbot")
    st.write(
        "This chatbot uses OpenAI's GPT-4.0 model alongside data from Jira to provide insights on ongoing projects."
    )

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to retrieve data from Jira
    def search_jira(query):
        # Use Basic Authentication with email and API token
        auth = (jira_email, jira_api_token)
        params = {"jql": query}  # JQL query to filter issues
        response = requests.get(f"{jira_url}/rest/api/2/search", auth=auth, params=params)
        
        if response.status_code == 200:
            # Display response for debugging
            st.write(response.json())  # Output the raw JSON response for troubleshooting
            return "\n".join(
                [issue["fields"]["summary"] + ": " + issue["fields"]["description"][:200]
                 for issue in response.json().get("issues", [])]
            )
        else:
            # Show error if request was not successful
            st.error(f"Failed to fetch data from Jira: {response.status_code}")
            st.write(response.text)  # Output error response text for further inspection

        return "No relevant information found in Jira."

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("Ask a question related to your Jira data"):

        # Store and display the current prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Collect data from Jira
        jira_data = search_jira("status != 'Done'")  # Modify JQL as needed for active projects

        # Compile Jira data for OpenAI
        compiled_data = f"Jira Data:\n{jira_data}"

        # Generate response using OpenAI with the latest API format
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing security insights."},
                {"role": "user", "content": f"{compiled_data}\n\nUser question: {prompt}"}
            ]
        ).choices[0].message['content']

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Store the assistant's response
        st.session_state.messages.append({"role": "assistant", "content": response})
