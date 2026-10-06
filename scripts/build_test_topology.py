from __future__ import annotations

import json
import sys
from pathlib import Path

import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def text_of(result) -> str:
    parts = []
    for item in result.content:
        if hasattr(item, "text"):
            parts.append(item.text)
    return "\n".join(parts)


async def main() -> None:
    params = StdioServerParameters(
        command=str(PYTHON),
        args=["-m", "packet_tracer_mcp", "--stdio"],
        cwd=str(ROOT),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            devices = text_of(await session.call_tool("pt_list_devices", {}))
            print(f"DISCOVERY_CHARS={len(devices)}")
            for model in ("2911", "2960-24TT", "PC-PT"):
                details = text_of(await session.call_tool("pt_get_device_details", {"model_name": model}))
                print(f"DETAILS_{model}={details}")

            plan = text_of(await session.call_tool(
                "pt_plan_topology",
                {
                    "routers": 1,
                    "switches_per_router": 1,
                    "pcs_per_lan": 2,
                    "laptops_per_lan": 0,
                    "servers": 0,
                    "access_points": 0,
                    "has_wan": False,
                    "dhcp": True,
                    "routing": "none",
                    "router_model": "2911",
                    "switch_model": "2960-24TT",
                    "template": "single_lan",
                    "lan_base": "192.168.10.0/24",
                },
            ))
            plan_path = ROOT / "projects" / "prueba_mcp_packet_tracer_plan.json"
            plan_path.parent.mkdir(exist_ok=True)
            plan_path.write_text(plan, encoding="utf-8")
            print(f"PLAN_PATH={plan_path}")

            plan_data = json.loads(plan)
            print("PLAN_SUMMARY=" + json.dumps({
                "devices": [d["name"] for d in plan_data["devices"]],
                "links": plan_data["links"],
                "dhcp_pools": plan_data["dhcp_pools"],
                "router_interfaces": [
                    {"name": d["name"], "interfaces": d["interfaces"]}
                    for d in plan_data["devices"]
                    if d["category"] == "router"
                ],
                "host_gateways": [
                    {"name": d["name"], "interfaces": d["interfaces"], "gateway": d["gateway"]}
                    for d in plan_data["devices"]
                    if d["category"] == "pc"
                ],
            }, indent=2))

            validation = text_of(await session.call_tool("pt_validate_plan", {"plan_json": plan}))
            print(f"VALIDATION={validation}")

            configs = text_of(await session.call_tool("pt_generate_configs", {"plan_json": plan}))
            configs_path = ROOT / "projects" / "prueba_mcp_packet_tracer_configs.txt"
            configs_path.write_text(configs, encoding="utf-8")
            print(f"CONFIGS_PATH={configs_path}")

            export = text_of(await session.call_tool(
                "pt_export",
                {
                    "plan_json": plan,
                    "project_name": "prueba_mcp_packet_tracer",
                    "output_dir": "projects",
                },
            ))
            print(f"EXPORT={export}")

            bridge = text_of(await session.call_tool("pt_bridge_status", {}))
            print(f"BRIDGE_STATUS={bridge}")


if __name__ == "__main__":
    anyio.run(main)
