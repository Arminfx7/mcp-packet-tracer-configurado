from __future__ import annotations

import anyio
import sys
from pathlib import Path
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main() -> None:
    root = Path(__file__).resolve().parents[1]
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "packet_tracer_mcp", "--stdio"],
        cwd=str(root),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            selected = {
                "pt_list_devices",
                "pt_get_device_details",
                "pt_plan_topology",
                "pt_validate_plan",
                "pt_fix_plan",
                "pt_generate_configs",
                "pt_full_build",
                "pt_export",
                "pt_bridge_status",
                "pt_live_deploy",
                "pt_verify_connectivity",
                "pt_save_project",
            }
            for tool in result.tools:
                print(tool.name)
                if tool.name in selected:
                    print(tool.inputSchema)
            print(f"TOTAL={len(result.tools)}")


if __name__ == "__main__":
    anyio.run(main)
