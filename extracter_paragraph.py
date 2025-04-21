import json
import requests
import csv
from time import sleep
import re

JSON_FILE = "llava_med_instruct_10k.json"
OLLAMA_URL = "http://10.18.224.73:11434/api/generate"
MODEL_NAME = "deepseek-r1"
OUTPUT_CSV = "dieases_info_extraction_20425.csv"

role = """
You are a clinical AI assistant designed to generate concise and medically 
relevant paragraph from vision-language conversations.

response format must be in the following format:
{
    "paragraph": "Your paragraph here",
}

Given the following conversation about a medical image, perform the following tasks:

Create paragraph of bot response.

1. **Include all relevant medical terms** with relevant organ and locations where
 found in the image with relation of each other mentioned in the conversation 
 (e.g., modality, anatomical terms, technical methods, evaluation metrics).
2. Ensure the paragraph captures:
   - The imaging modality
   - The anatomical region under analysis
   - Key performance metrics, if mentioned
   - Any specific disease terms (if present)
   - Any Ogran or location mentioned in the conversation

**Format the output in plain text. Do not include explanations.** Only return the final paragraph.

give response in the following format:
```
{
    "paragraph": "Your paragraph here",
}
```
Now analyze the following conversation:
"""

def extract_conversation_text(conversations):
    lines = []
    for item in conversations:
        sender = item["from"]
        message = item["value"]
        lines.append("{}: {}".format(sender, message))
    return "\n".join(lines)

def call_ollama(role,conversation_text):
    full_prompt = role + conversation_text
    try:
        extracted_text = ""

        for i in range(5):
  
            if i > 1:
                full_prompt = "You have not provided a valid response in json format. Please try again.\n" + role + conversation_text
            
            response = requests.post(OLLAMA_URL, json={
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False
            })
            response.raise_for_status()
            raw_text = response.json().get("response", "")

            # print("Raw response: {}".format(raw_text))
            try:
                extracted_text = re.search(r'{\s*"paragraph":\s*"(.*?)"\s*}', raw_text, re.DOTALL).group(1)
                break
            except AttributeError:
                extracted_text = "no format found"

        return extracted_text

    except Exception as e:
        print("Error during Ollama call: {}".format(e))
        return []

def main():
    i = 0
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
        with open(OUTPUT_CSV, mode='w', newline='') as file:

            writer = csv.DictWriter(file, fieldnames=["image_id", "info"])
            writer.writeheader()

            buffer = []
            save_interval = 5  

            for idx, entry in enumerate(data, start=1):

                i += 1

                image_id = entry["id"]
                print("Processing Image ID: {} : {}".format(image_id,i))

                conversation_text = extract_conversation_text(entry["conversatons"])
                info = call_ollama(role, conversation_text)
           
                # print("Verification Info: {}".format(info))
                # break
                buffer.append({
                    "image_id": image_id,
                    "info": info
                })
     
                if idx % save_interval == 0:
                    writer.writerows(buffer)
                    file.flush()
                    buffer.clear()
                    print("Saved progress up to entry {}".format(idx))
                #break
                sleep(0.5)

            if buffer:
                writer.writerows(buffer)
                print("Saved remaining entries.")

if __name__ == "__main__":
    main()