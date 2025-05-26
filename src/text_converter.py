import json
import pandas as pd
from io import StringIO

def text_to_json(text_content: str) -> str:
    """Converts a string to a JSON string with a 'text' field."""
    return json.dumps({"text": text_content}, indent=4)

def text_to_csv(text_content: str) -> str:
    """Converts a string to a CSV formatted string with a 'text' column."""
    # Use a dictionary to create a DataFrame, which is an easy way to structure data for CSV
    df = pd.DataFrame([{"text": text_content}])
    # Use StringIO to capture CSV output from pandas
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

if __name__ == '__main__':
    sample_text = "This is a sample piece of text for conversion."

    # Test JSON conversion
    json_output = text_to_json(sample_text)
    print("------ JSON Output ------")
    print(json_output)

    # Test CSV conversion
    csv_output = text_to_csv(sample_text)
    print("\n------ CSV Output ------")
    print(csv_output)

    # Verify direct CSV output for a simple case
    # print(pd.DataFrame([{"text": "line1"}, {"text": "line2"}]).to_csv(index=False))
