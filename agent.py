import os
import sys
import requests

def run_agent():
    # 1. Read environment variables and Issue details
    api_key = os.getenv("DEEPSEEK_API_KEY")
    issue_title = os.getenv("ISSUE_TITLE", "")
    issue_body = os.getenv("ISSUE_BODY", "")
    
    if not api_key:
        print("Error: Missing DEEPSEEK_API_KEY environment variable!")
        sys.exit(1)

    # 2. Read the existing context (main.py)
    with open("main.py", "r") as f:
        current_code = f.read()

    # 3. Construct the prompt for DeepSeek
    prompt = f"""
    You are an expert Python developer. Your task is to modify the 'main.py' file based on the GitHub Issue provided below.
    
    Current code in 'main.py':
```python
    {current_code}
    ```
    
    GitHub Issue:
    Title: {issue_title}
    Description: {issue_body}
    
    CRITICAL INSTRUCTION: Return ONLY the final, modified Python code. Do NOT wrap it in markdown code blocks (```python) and do NOT include any explanation, comments, or introductory text. Just the executable Python code.
    """

    # 4. Call the DeepSeek API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    print("Starting AI Agent... Generating plan using DeepSeek model...")
    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"API Error: {response.text}")
        sys.exit(1)
        
    ai_code = response.json()['choices'][0]['message']['content'].strip()

    # 5. Write the modified code back to main.py
    with open("main.py", "w") as f:
        f.write(ai_code)
    
    print("Code successfully updated by the AI Agent!")

if __name__ == "__main__":
    run_agent()
