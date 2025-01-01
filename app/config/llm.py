from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-1.5-flash",google_api_key="AIzaSyAdqWn3x7DBe9stQbR4OASbqVJ6UoafDNg",generation_config={"response_mime_type": "application/json"})



