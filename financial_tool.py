from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import json
import pandas as pd
api_key = 'jsijs'


client = MistralClient(api_key=api_key)


def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    model = "mistral-large-latest"
    messages = [ChatMessage(role="user", content=prompt)]
    
    try:
        chat_response = client.chat(
            model=model,
            messages=messages
        )
        reply = chat_response.choices[0].message.content
        
        # Debugging: print the reply to inspect its content
        print("Reply from Mistral:", reply)

        # Remove code block markers if present
        reply = reply.strip()
        if reply.startswith("```json"):
            reply = reply[7:].strip()  # Remove starting ```json and extra spaces
        if reply.endswith("```"):
            reply = reply[:-3].strip()  # Remove ending ```

        # Try to parse the cleaned JSON
        data = json.loads(reply)
        
        # Ensure all necessary fields are present in the JSON response
        expected_keys = ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"]
        data = {key: data.get(key, "") for key in expected_keys}
        
        # Convert to DataFrame
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing JSON or missing data: {e}")
        # Return an empty DataFrame with the correct structure
        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })

# Function to generate the prompt for extracting financial data
def get_prompt_financial():
    return """Please retrieve company name, revenue, net income, and 
    earnings per share (a.k.a EPS) from the following news article.
    If you can't find the information from this article, then return nothing.
    Do not make things up. Then retrieve a stock symbol corresponding to that company.
    For this, you can use your general knowledge (it doesn't have to be from this article).
    Always return your response as a valid JSON string.
    The format of that string should be this,
    {"Company Name": "Walmart",
    "Stock Symbol": "WMT",
    "Revenue": "12.34 million",
    "Net Income": "34.78",
    "EPS": "2.1$"
    }

    News Article
    ===========================
    """

text = '''
    Tesla's Earning news in text format: Tesla's earning this quarter blew all the estimates. They reported 4.5 billion $ profit against a revenue of 30 billion $. Their earnings per share was 2.3 $
    '''
df = extract_financial_data(text)

print(df.to_string())