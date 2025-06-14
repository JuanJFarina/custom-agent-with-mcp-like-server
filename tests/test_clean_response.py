from custom_agent_with_mcp_like_server.clean_response import clean_response

def test_clean_response():
    bad_response = "```json{}```"
    cleaned_response = clean_response(bad_response)
    assert cleaned_response == "{}"