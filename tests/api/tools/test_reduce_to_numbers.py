from custom_agent_with_mcp_like_server.api import reduce_to_numbers

def test_reduce_to_numbers() -> None:
    assert reduce_to_numbers("abc") == "123"
    assert reduce_to_numbers("def") == "456"
    assert reduce_to_numbers("ghi") == "789"
