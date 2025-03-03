import sys
import requests

GITHUB_API_URL = "https://api.github.com/users/{username}/events"

def fetch_events(username):
    url = GITHUB_API_URL.format(username=username)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_events(events):
    push_count = 0
    results = []

    for event in events:
        repo_name = event["repo"]["name"]
        event_type = event["type"]

        if event["type"] == "PushEvent":
            push_count += 1        
        else:
            if push_count > 0:
                results.append(f"- pushed {push_count} commit(s) to {repo_name}")
                push_count = 0

            event_description = get_event_description(event_type, repo_name)
            if event_description:
                results.append(event_description)

    # Handle remaining push events
    if push_count > 0:
        results.append(f"pushed {push_count} commits to {repo_name}")

    return results

def get_event_description(event_type, repo):
    description = {
        "PublicEvent": f"- changed to public: {repo}",
        "CreateEvent": f"- created: {repo}",
        "WatchEvent": f"- watched: {repo}",
        "PullRequestEvent": f"- requested pull from: {repo}",
        "IssueCommentEvent": f"- commented an issue: {repo}",
        "IssuesEvent": f"- issued: {repo}",
        "ForkEvent": f"- forked: {repo}",
        "DeleteEvent": f"- deleted: {repo}"
    }
    return description.get(event_type, f"* unknown type: {event_type}")

def print_results(results):
    for result in results:
        print(result)

def main(username):
    events = fetch_events(username)
    if events:
        results = process_events(events)
        print_results(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        main(username)
    else:
        print("Please provide a GitHub username as an argument.")
