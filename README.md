# README

## Overview

This project provides a Python-based solution for named entity recognition (NER), specifically identifying personal names (ФИО) in Russian texts. It uses OpenAI's GPT-4 model via the `langchain` framework to extract names from input texts, retaining their original case and position. The solution consists of three main scripts:

1. **`model.py`**: Defines the language model pipeline for entity extraction.
2. **`main.py`**: Implements a cloud-hosted service for processing text and extracting entities.
3. **`test.py`**: Provides testing and evaluation metrics for the entity extraction performance.

## File Descriptions

### 1. `model.py`

- **Purpose**: Defines the pipeline for extracting personal names from text.
- **Key Components**:
  - Uses `ChatOpenAI` from `langchain_openai` to initialize the GPT-4 model.
  - Constructs a prompt to identify all names (ФИО) within a given text.
  - Defines an asynchronous function, `generate_answer()`, which processes the text to extract names and their positions.
  
### 2. `main.py`

- **Purpose**: Implements the NER service as a cloud-hosted API.
- **Key Components**:
  - `SimpleActionExample` class defines the service logic for entity extraction using the model pipeline from `model.py`.
  - Takes input texts, processes them to extract entities, and formats the results according to predefined schemas.
  - Uses `mlp_sdk` to handle API hosting and deployment.

### 3. `test.py`

- **Purpose**: Tests and evaluates the entity extraction performance.
- **Key Components**:
  - Downloads a dataset of annotated texts to test the NER functionality.
  - Computes precision, recall, and F1-score metrics for the model output.
  - Supports running tests on a configurable number of files using command-line arguments.

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

### Running the NER Service

To start the entity extraction service:

```bash
python main.py
```
This will host the NER service using mlp_sdk on the cloud.

### Running Tests

To evaluate the performance of the NER model:
```bash
python test.py --count <number_of_files>
```

Replace <**number_of_files**> with the number of test files you wish to evaluate.

##Example

To extract entities from the text:
1. **Input Text:** Гагарин полетел на орбиту на ракете Сергея Королёва.
2. **Output:** 
```json 
{
  "entities_list": [
    {
      "entities": [
        {
          "value": "Гагарин",
          "entity_type": "PERSON",
          "span": {
            "start_index": 0,
            "end_index": 7
          },
          "entity": "Гагарин",
          "source_type": "SLOVNET"
        },
        {
          "value": "Сергея Королёва",
          "entity_type": "PERSON",
          "span": {
            "start_index": 28,
            "end_index": 42
          },
          "entity": "Сергея Королёва",
          "source_type": "SLOVNET"
        }
      ]
    }
  ]
}
```

## Evaluation metrics
- **Precision:** Measures the accuracy of the names extracted by the model.
- **Recall:** Measures the coverage of the model in identifying all relevant names.
- **F1 Score:** Harmonic mean of precision and recall, providing a balanced evaluation metric.