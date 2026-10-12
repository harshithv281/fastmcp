"""Feature-gap demo: a timed-out sync tool's worker thread is not stopped."""
import asyncio
import sys
import importlib.metadata
import time
from datetime import datetime

from fastmcp import Client, FastMCP

mcp = FastMCP("thread-demo")


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


@mcp.tool(timeout=1.0)
def long_tool() -> str:
    for step in range(1, 6):
        time.sleep(1)
        print(f"[{ts()}] tool: still working, step {step}", flush=True)
    print(f"[{ts()}] tool: finished all 5 steps", flush=True)
    return "done"


async def main() -> None:
    print(f"fastmcp version: {importlib.metadata.version('fastmcp')}")
    # Optional: --client-timeout also sets a 1.0s timeout on the client side.
    client_timeout = 1.0 if "--client-timeout" in sys.argv else None
    print(f"[{ts()}] client: calling long_tool "
          f"(tool timeout=1.0, client timeout={client_timeout})")
    start = time.perf_counter()
    async with Client(mcp) as client:
        try:
            result = await client.call_tool(
                "long_tool", {}, timeout=client_timeout
            )
            print(f"[{ts()}] client: SUCCESS {result.data!r} "
                  f"after {time.perf_counter() - start:.2f}s")
        except Exception as e:
            print(f"[{ts()}] client: got ERROR after "
                  f"{time.perf_counter() - start:.2f}s -> {type(e).__name__}: {e}")
        print(f"[{ts()}] client: waiting 6s to see if the tool keeps running...")
        await asyncio.sleep(6)
    print(f"[{ts()}] client: done waiting")


if __name__ == "__main__":
    asyncio.run(main())
