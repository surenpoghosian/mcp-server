import asyncio
import json
import subprocess
import sys

async def test_server():
    # Start the server process
    process = await asyncio.create_subprocess_exec(
        sys.executable, "src/server.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Send initialization request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    # Send request
    request_str = json.dumps(init_request) + "\n"
    process.stdin.write(request_str.encode())
    await process.stdin.drain()
    
    # Read response
    response = await process.stdout.readline()
    print("Response:", response.decode().strip())
    
    # Clean up
    process.terminate()
    await process.wait()

if __name__ == "__main__":
    asyncio.run(test_server())
