from src.clean_response import clean_response

def test_clean_response():
    bad_response = "```json{}```"
    cleaned_response = clean_response(bad_response)
    assert cleaned_response == "{}"