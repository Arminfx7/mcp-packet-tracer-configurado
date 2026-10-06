from __future__ import annotations

import json
import sys
from pathlib import Path

import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)
OUT_DIR = ROOT / "projects"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def content_text(result) -> str:
    return "\n".join(getattr(item, "text", "") for item in result.content)


def device(name: str, model: str, category: str, x: int, y: int, interfaces=None, gateway="", vlan=0):
    return {
        "name": name,
        "model": model,
        "category": category,
        "role": "end_host" if category in {"pc", "server", "laptop"} else (
            "core_router" if category == "router" else "access_switch"
        ),
        "x": x,
        "y": y,
        "interfaces": interfaces or {},
        "gateway": gateway,
        "interfaces_v6": {},
        "gateway_v6": "",
        "vlan": vlan,
        "wireless": False,
    }


def link(a: str, pa: str, b: str, pb: str, cable: str = "straight"):
    return {"device_a": a, "port_a": pa, "device_b": b, "port_b": pb, "cable": cable}


def access(sw: str, port: str, vlan: int):
    return {"switch": sw, "port": port, "vlan_id": vlan}


def trunk(sw: str, port: str):
    return {"switch": sw, "port": port, "allowed_vlans": [10, 20, 30, 40, 50], "native_vlan": 1, "encapsulation": "dot1q"}


PLAN = {
    "name": "ejercicio_umg_canvas",
    "devices": [
        device("R1", "2911", "router", 520, 190, {
            "GigabitEthernet0/0.10": "192.168.1.1/24",
            "GigabitEthernet0/0.20": "192.168.2.1/24",
            "GigabitEthernet0/0.30": "192.168.3.1/24",
            "GigabitEthernet0/0.40": "192.168.4.1/24",
            "GigabitEthernet0/0.50": "192.168.5.1/24",
        }),
        device("SW-Core", "3560-24PS", "switch", 520, 300),
        device("SW-Servidores-1", "2960-24TT", "switch", 230, 190),
        device("SW-Nivel-1", "2960-24TT", "switch", 330, 430),
        device("SW-Nivel-2", "2960-24TT", "switch", 520, 455),
        device("SW-Nivel-3", "2960-24TT", "switch", 710, 430),
        device("SW-Servidores-2", "2960-24TT", "switch", 805, 190),
        device("Servidor-DNS", "Server-PT", "server", 75, 145, {"FastEthernet0": "192.168.1.10/24"}, "192.168.1.1", 10),
        device("Servidor-FTP", "Server-PT", "server", 75, 240, {"FastEthernet0": "192.168.1.20/24"}, "192.168.1.1", 10),
        device("Servidor-Correo-UMG", "Server-PT", "server", 210, 330, {"FastEthernet0": "192.168.1.30/24"}, "192.168.1.1", 10),
        device("PC4", "PC-PT", "pc", 220, 585, {"FastEthernet0": "192.168.2.10/24"}, "192.168.2.1", 20),
        device("PC5", "PC-PT", "pc", 320, 585, {"FastEthernet0": "192.168.2.11/24"}, "192.168.2.1", 20),
        device("PC6", "PC-PT", "pc", 405, 585, {"FastEthernet0": "192.168.2.12/24"}, "192.168.2.1", 20),
        device("Laptop0", "Laptop-PT", "laptop", 430, 620, {"FastEthernet0": "192.168.3.10/24"}, "192.168.3.1", 30),
        device("Laptop1", "Laptop-PT", "laptop", 525, 610, {"FastEthernet0": "192.168.3.11/24"}, "192.168.3.1", 30),
        device("Laptop2", "Laptop-PT", "laptop", 620, 610, {"FastEthernet0": "192.168.3.12/24"}, "192.168.3.1", 30),
        device("PC7", "PC-PT", "pc", 640, 585, {"FastEthernet0": "192.168.4.10/24"}, "192.168.4.1", 40),
        device("Laptop3", "Laptop-PT", "laptop", 735, 575, {"FastEthernet0": "192.168.4.11/24"}, "192.168.4.1", 40),
        device("Laptop4", "Laptop-PT", "laptop", 830, 575, {"FastEthernet0": "192.168.4.12/24"}, "192.168.4.1", 40),
        device("Servidor-UMG", "Server-PT", "server", 970, 135, {"FastEthernet0": "192.168.5.10/24"}, "192.168.5.1", 50),
        device("Servidor-Canvas", "Server-PT", "server", 980, 235, {"FastEthernet0": "192.168.5.20/24"}, "192.168.5.1", 50),
        device("Servidor-Correo-Canvas", "Server-PT", "server", 980, 345, {"FastEthernet0": "192.168.5.30/24"}, "192.168.5.1", 50),
    ],
    "modules": [],
    "links": [
        link("R1", "GigabitEthernet0/0", "SW-Core", "GigabitEthernet0/1"),
        link("SW-Core", "FastEthernet0/1", "SW-Servidores-1", "GigabitEthernet0/1", "cross"),
        link("SW-Core", "FastEthernet0/2", "SW-Nivel-1", "GigabitEthernet0/1", "cross"),
        link("SW-Core", "FastEthernet0/3", "SW-Nivel-2", "GigabitEthernet0/1", "cross"),
        link("SW-Core", "FastEthernet0/4", "SW-Nivel-3", "GigabitEthernet0/1", "cross"),
        link("SW-Core", "FastEthernet0/5", "SW-Servidores-2", "GigabitEthernet0/1", "cross"),
        link("SW-Servidores-1", "FastEthernet0/1", "Servidor-DNS", "FastEthernet0"),
        link("SW-Servidores-1", "FastEthernet0/2", "Servidor-FTP", "FastEthernet0"),
        link("SW-Servidores-1", "FastEthernet0/3", "Servidor-Correo-UMG", "FastEthernet0"),
        link("SW-Nivel-1", "FastEthernet0/1", "PC4", "FastEthernet0"),
        link("SW-Nivel-1", "FastEthernet0/2", "PC5", "FastEthernet0"),
        link("SW-Nivel-1", "FastEthernet0/3", "PC6", "FastEthernet0"),
        link("SW-Nivel-2", "FastEthernet0/1", "Laptop0", "FastEthernet0"),
        link("SW-Nivel-2", "FastEthernet0/2", "Laptop1", "FastEthernet0"),
        link("SW-Nivel-2", "FastEthernet0/3", "Laptop2", "FastEthernet0"),
        link("SW-Nivel-3", "FastEthernet0/1", "PC7", "FastEthernet0"),
        link("SW-Nivel-3", "FastEthernet0/2", "Laptop3", "FastEthernet0"),
        link("SW-Nivel-3", "FastEthernet0/3", "Laptop4", "FastEthernet0"),
        link("SW-Servidores-2", "FastEthernet0/1", "Servidor-UMG", "FastEthernet0"),
        link("SW-Servidores-2", "FastEthernet0/2", "Servidor-Canvas", "FastEthernet0"),
        link("SW-Servidores-2", "FastEthernet0/3", "Servidor-Correo-Canvas", "FastEthernet0"),
    ],
    "dhcp_pools": [],
    "static_routes": [],
    "ospf_configs": [],
    "rip_configs": [],
    "eigrp_configs": [],
    "vlans": [
        {"vlan_id": 10, "name": "SERVIDORES_UMG", "subnet": "192.168.1.0/24"},
        {"vlan_id": 20, "name": "NIVEL_1", "subnet": "192.168.2.0/24"},
        {"vlan_id": 30, "name": "NIVEL_2", "subnet": "192.168.3.0/24"},
        {"vlan_id": 40, "name": "NIVEL_3", "subnet": "192.168.4.0/24"},
        {"vlan_id": 50, "name": "SERVIDORES_CANVAS", "subnet": "192.168.5.0/24"},
    ],
    "access_ports": [
        access("SW-Servidores-1", "FastEthernet0/1", 10), access("SW-Servidores-1", "FastEthernet0/2", 10), access("SW-Servidores-1", "FastEthernet0/3", 10),
        access("SW-Nivel-1", "FastEthernet0/1", 20), access("SW-Nivel-1", "FastEthernet0/2", 20), access("SW-Nivel-1", "FastEthernet0/3", 20),
        access("SW-Nivel-2", "FastEthernet0/1", 30), access("SW-Nivel-2", "FastEthernet0/2", 30), access("SW-Nivel-2", "FastEthernet0/3", 30),
        access("SW-Nivel-3", "FastEthernet0/1", 40), access("SW-Nivel-3", "FastEthernet0/2", 40), access("SW-Nivel-3", "FastEthernet0/3", 40),
        access("SW-Servidores-2", "FastEthernet0/1", 50), access("SW-Servidores-2", "FastEthernet0/2", 50), access("SW-Servidores-2", "FastEthernet0/3", 50),
    ],
    "trunks": [
        trunk("SW-Core", "GigabitEthernet0/1"),
        trunk("SW-Core", "FastEthernet0/1"),
        trunk("SW-Core", "FastEthernet0/2"),
        trunk("SW-Core", "FastEthernet0/3"),
        trunk("SW-Core", "FastEthernet0/4"),
        trunk("SW-Core", "FastEthernet0/5"),
        trunk("SW-Servidores-1", "GigabitEthernet0/1"),
        trunk("SW-Nivel-1", "GigabitEthernet0/1"),
        trunk("SW-Nivel-2", "GigabitEthernet0/1"),
        trunk("SW-Nivel-3", "GigabitEthernet0/1"),
        trunk("SW-Servidores-2", "GigabitEthernet0/1"),
    ],
    "subinterfaces": [
        {"router": "R1", "parent_port": "GigabitEthernet0/0", "vlan_id": 10, "ip_cidr": "192.168.1.1/24", "encapsulation": "dot1Q"},
        {"router": "R1", "parent_port": "GigabitEthernet0/0", "vlan_id": 20, "ip_cidr": "192.168.2.1/24", "encapsulation": "dot1Q"},
        {"router": "R1", "parent_port": "GigabitEthernet0/0", "vlan_id": 30, "ip_cidr": "192.168.3.1/24", "encapsulation": "dot1Q"},
        {"router": "R1", "parent_port": "GigabitEthernet0/0", "vlan_id": 40, "ip_cidr": "192.168.4.1/24", "encapsulation": "dot1Q"},
        {"router": "R1", "parent_port": "GigabitEthernet0/0", "vlan_id": 50, "ip_cidr": "192.168.5.1/24", "encapsulation": "dot1Q"},
    ],
    "validations": [
        {"check_type": "ping", "from_device": "PC4", "to_target": "Servidor-Canvas", "expected": "Reply"},
        {"check_type": "ping", "from_device": "Laptop0", "to_target": "Servidor-DNS", "expected": "Reply"},
    ],
    "dual_stack": False,
    "errors": [],
    "warnings": [],
}


async def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    plan_json = json.dumps(PLAN, indent=2)
    (OUT_DIR / "ejercicio_umg_canvas_plan.json").write_text(plan_json, encoding="utf-8")

    params = StdioServerParameters(
        command=str(PYTHON),
        args=["-m", "packet_tracer_mcp", "--stdio"],
        cwd=str(ROOT),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("bridge:", content_text(await session.call_tool("pt_bridge_status", {})))
            print("validate:", content_text(await session.call_tool("pt_validate_plan", {"plan_json": plan_json})))
            print("deploy:", content_text(await session.call_tool("pt_live_deploy", {"plan_json": plan_json, "command_delay": 0.05})))
            print("topology:", content_text(await session.call_tool("pt_query_topology", {})))
            checks = [
                ("PC4", "192.168.5.20"),
                ("Laptop0", "192.168.1.10"),
                ("Servidor-DNS", "192.168.5.30"),
            ]
            for source, target in checks:
                print("ping:", content_text(await session.call_tool("pt_verify_connectivity", {"from_device": source, "to_ip": target, "timeout_s": 60})))
            print("save:", content_text(await session.call_tool(
                "pt_save_project",
                {"filename": "ejercicio_umg_canvas.pkt", "directory": str(OUT_DIR)},
            )))


if __name__ == "__main__":
    anyio.run(main)
