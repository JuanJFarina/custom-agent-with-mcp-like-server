def clean_response(response: str) -> str:
    cleaned_response = response.strip(response.split("{", maxsplit=1)[0])
    print(f"Cleaned_response after split = {cleaned_response}")
    cleaned_response = cleaned_response.strip(cleaned_response.rsplit("}", maxsplit=1)[1])
    print(f"Cleaned_response after rsplit = {cleaned_response}")
    cleaned_response = cleaned_response.replace("\n", "\\n")
    cleaned_response = cleaned_response.replace("\t", "\\t")
    return cleaned_response.replace("\r", "\\r")
