from dotenv import load_dotenv
import os
import google.generativeai as genai


class ContentCreator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

    def generate(self, transcript):
        generation_config = {"temperature": 0.55, "top_p":0.7, "top_k":1, "max_output_tokens":99999}
        model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
        try:
            summary_prompt = f"""
```
{transcript}
```
Please summarize the following transcript to highlight the key points and main ideas. The summary should be concise and engaging, designed specifically for creating social media reels. Focus on making it attention-grabbing, while preserving the essence of the content.
"""

            summary_response = model.generate_content(f"{summary_prompt}")

            prompt1 = f"""
Summary:
```
{summary_response.text}
```

I have a YouTube video transcript's summary, and I want to transform it into a series of engaging, platform-optimized short-form videos (Reels, Shorts). Your task is to analyze the transcript, Extract the core idea and create multiple relevant, concise, attention-grabbing scripts that:
1. Highlight unique, powerful ideas or moments from the transcript.
2. Use hook-driven storytelling techniques to immediately capture attention.
3. Incorporate engaging narrative elements, such as:
    - Unexpected revelations
    - Personal anecdotes
    - Provocative questions
    - Clear, actionable takeaways

For each script, provide:
- A suggested opening hook (5-10 seconds). This should grab attention immediately.
- Main content (120-150 words). Break down the key message or idea in a clear and engaging way, with a focus on clarity and simplicity. Ensure the main content is around 120-150 words so it fits into a 1-minute reel.
    - The language should be short, punchy, and easy to read, suitable for quick consumption.
    - Include at least one actionable takeaway or piece of advice.
    - Aim for no more than 3 main points in a single paragraph, keeping each idea brief but impactful.
- Call of action on the basis of script in about 50 words (eg. if something is critisized then tell how to tackle it)
- Ensure the tone is consistent with the video’s original style (educational, motivational, entertaining) and that the scripts are optimized for platform-specific engagement. Divide the transcript into clear, impactful sections to create distinct scripts, each with a clear call to action that drives audience interaction or retention.
- The main content should not have any suggestions or anything it should be totally from transcript and only the call of action should contain suggestions if required

Divide the transcript into distinct, self-contained sections that could each serve as an individual script for a reel. Each section should focus on a unique idea or message.
"""
            
            response1 = model.generate_content(f"{prompt1}")

            prompt2 = f"""
```
{response1.text}
```

I noticed that in the previous response, the main content was too brief. Based on this feedback, please provide me with a more detailed reading script that is around 300 words for each reel content created above. Additionally, include 80 words for the call-to-action for each reel.
"""

            response2 = model.generate_content(prompt2)
            return summary_response.text, response1.text, response2.text
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    proj = "EDU-1"
    creator = ContentCreator()
    with open("text2.txt", 'r') as file:
        transcript = file.read()

    output = creator.generate(transcript)
    print(output)
    with open(f"projects/{proj}/scripts3.txt", 'w', encoding='utf-8') as file:
        file.write(output)
