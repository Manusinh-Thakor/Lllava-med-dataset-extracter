# LLaVA-Med Data Extractor

## 📌 Purpose

This project is designed to extract structured, informative paragraphs from the **LLaVA-Med dataset**, a vision-language conversation dataset for medical applications. The script processes conversations between a human and an AI assistant discussing medical images and generates a **medically-relevant summary paragraph** for each entry.

It is mainly intended to support downstream tasks such as:
- Building structured knowledge bases from unstructured medical dialogues
- Preprocessing data for retrieval-augmented generation (RAG) systems
- Generating training/evaluation data for VQA and diagnostic assistants

---

## 🛠️ Files

- `extracter_paragraph.py`: Main script for extracting a structured paragraph from conversations using an API call to a local Ollama server.
- `extracter_name_only.py`: A minimal model usage example for MedPalm (not used in the main extraction flow).

---

## 🔧 How to Use

### 1. Requirements

Ensure the following are available:
- Python 3.7+
- Ollama server running with a model (e.g., `deepseek-r1`)
- `llava_med_instruct_10k.json` file in the working directory

### 2. Configure the script

Open `extracter_paragraph.py` and check the configuration at the top:
```python
JSON_FILE = "llava_med_instruct_10k.json"   # Input file
OLLAMA_URL = "http://<your_ollama_host>:11434/api/generate"  # Change to your Ollama instance
MODEL_NAME = "deepseek-r1"  # Replace with your loaded model name
OUTPUT_CSV = "dieases_info_extraction_20425.csv"  # Output file
```

### 3. Run the script

```bash
python extracter_paragraph.py
```

This will:
- Load and iterate through the conversation entries
- Extract a structured paragraph from the conversation using a prompt template
- Save output as a CSV with columns: `image_id`, `info`

---

## 🧪 Output Format

The output CSV (`dieases_info_extraction_20425.csv`) contains:

| image_id         | info                                      |
|------------------|-------------------------------------------|
| 26597251_Fig1    | "This image shows a CT scan of..."        |
| ...              | ...                                       |

---

## 📝 Notes

- The model is prompted to **only return a JSON object** with a single key: `"paragraph"`.
- The script automatically retries if the response is not in valid JSON format.
- It saves progress periodically in case of interruption.

