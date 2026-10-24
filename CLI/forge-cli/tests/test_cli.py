import argparse

def test_cli_parser_setup():
    parser = argparse.ArgumentParser(description="ONGISA CLI")
    parser.add_argument("command", choices=["analyze", "audit", "chat"])
    
    args = parser.parse_args(["audit"])
    assert args.command == "audit"