import json
import os


def generate_startup_script():
    """
    Reads mcp.json and generates a batch file to start all servers.
    """
    try:
        with open("mcp.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: mcp.json not found in the current directory.")
        return
    except json.JSONDecodeError:
        print("Error: Could not parse mcp.json.")
        return

    servers = config.get("servers", {})
    if not servers:
        print("No servers found in mcp.json.")
        return

    script_path = "start_mcp_servers.bat"
    with open(script_path, "w") as f:
        f.write("@echo off\n")
        f.write("echo Starting MCP servers...\n\n")

        for name, server_config in servers.items():
            command = server_config.get("command")
            args = server_config.get("args", [])

            if not command:
                continue

            # Ensure args are strings and handle potential quoting issues
            str_args = " ".join(
                [f'"{arg}"' if " " in str(arg) else str(arg) for arg in args]
            )
            full_command = f"{command} {str_args}".strip()

            f.write(f"echo Starting server: {name}\n")
            f.write(f'start "{name}" cmd /k {full_command}\n')

        f.write("\necho All MCP servers are starting in separate windows.\n")

    print(f"Successfully generated {script_path}")


if __name__ == "__main__":
    generate_startup_script()
