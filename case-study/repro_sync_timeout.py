"""Repro for FastMCP bug #5378: timeout on a sync tool is not enforced."""
import asyncio
import importlib.metadata
import time

from fastmcp import Client, FastMCP

mcp = FastMCP("timeout-repro")


@mcp.tool(timeout=1.0)
def slow_tool() -> str:
    time.sleep(3)
    return "late result"


async def main() -> None:
    print(f"fastmcp version: {importlib.metadata.version('fastmcp')}")
    start = time.perf_counter()
    try:
        async with Client(mcp) as client:
            result = await client.call_tool("slow_tool", {})
        elapsed = time.perf_counter() - start
        print(f"elapsed: {elapsed:.2f}s")
        print(f"SUCCESS: {result.data!r}")
    except Exception as e:
        elapsed = time.perf_counter() - start
        print(f"elapsed: {elapsed:.2f}s")
        print(f"ERROR: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
