<div align="center">

<img src="demo/mcp-packet-tracer-banner.svg" alt="MCP Packet Tracer — automatización de topologías Cisco" width="100%"/>

**Tell your AI _"create a network with 3 routers, OSPF and DHCP"_ — it plans, validates, generates, and deploys the topology directly into Cisco Packet Tracer in real time.**

[![Version](https://img.shields.io/badge/version-0.6.0-blue?style=flat-square)](https://github.com/Mats2208/MCP-Packet-Tracer/releases)
[![Python](https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![MCP](https://img.shields.io/badge/protocol-MCP-00B4D8?style=flat-square)](https://modelcontextprotocol.io)
[![Website](https://img.shields.io/badge/website-mcpnetwork.top-0A66C2?style=flat-square&logo=googlechrome&logoColor=white)](https://www.mcpnetwork.top)
[![Docs](https://img.shields.io/badge/docs-mats2208.github.io-4051B5?style=flat-square&logo=materialformkdocs&logoColor=white)](https://mats2208.github.io/MCP-Packet-Tracer/)
[![License](https://img.shields.io/github/license/Mats2208/MCP-Packet-Tracer?style=flat-square&color=green)](https://github.com/Mats2208/MCP-Packet-Tracer/blob/main/LICENSE)

[![MCP Registry](https://lobehub.com/badge/mcp/mats2208-mcp-packet-tracer)](https://lobehub.com/mcp/mats2208-mcp-packet-tracer)

<br/>

<table>
<tr>
<td align="center"><strong>46 MCP Tools</strong></td>
<td align="center"><strong>5 MCP Resources</strong></td>
<td align="center"><strong>74 Device Models</strong></td>
<td align="center"><strong>151 Modules</strong></td>
<td align="center"><strong>15 Cable Types</strong></td>
</tr>
</table>

**🌐 Website:** https://www.mcpnetwork.top &nbsp;•&nbsp; **📚 Documentation:** https://mats2208.github.io/MCP-Packet-Tracer/

</div>

---

---

## What it does

## Configuraciones de laboratorio incluidas

Esta copia incluye proyectos de Cisco Packet Tracer listos para abrir en la carpeta [`projects/`](projects/):

- [`topologia_RIP_5_routers.pkt`](projects/topologia_RIP_5_routers.pkt): anillo de cinco routers con RIP v2, cinco LAN y dos PCs por LAN.
- [`topologia_excel_tipoA_tipoB.pkt`](projects/topologia_excel_tipoA_tipoB.pkt): topología basada en el ejercicio de subneteo.

Consulta [`INSTALACION.md`](INSTALACION.md) para instalar el MCP y [`CREDITOS.md`](CREDITOS.md) para conocer la procedencia del código y las referencias utilizadas.

A **Model Context Protocol (MCP) server** para usar desde ChatGPT/Codex u otro cliente de chat compatible con MCP, con control programático de Cisco Packet Tracer.

| | Feature | Details |
|---|---------|---------|
| **Planning** | Natural language → topology | A single prompt becomes a complete `TopologyPlan` |
| **IP / DHCP** | Auto /24 LANs + /30 links, DHCP pools | Sequential, gateway at `.1` |
| **Routing** | Static · OSPF · EIGRP · RIP | Full IOS generation |
| **Switching** | VLANs, trunks, **inter-VLAN routing** (router-on-a-stick), STP, port-security | `.1q` subinterfaces + per-VLAN DHCP |
| **Security** | Device hardening (SSH, local users, enable-secret, banner), ACL/NAT | On live devices via the bridge |
| **IPv6** | Dual-stack addressing | Routers via CLI, hosts via SLAAC |
| **Wireless** | WiFi laptops + auto-associated Access Points | NIC swap → `Wireless0`, default-SSID assoc |
| **Validation** | Typed errors + auto-fixer | Wrong cables, missing ports, model upgrades |
| **Verification** | Plan-vs-live diff, health check, **real ping** (`pt_verify_connectivity`) | Drift, down links, duplicate IPs — and actual reachability |
| **Deploy** | Real-time bridge to PT (auto-reconciles) | No copy-paste — commands stream directly |
| **Two channels** | HTTP when the extension window is open, **file-bridge when it's closed** | PT keeps executing with the window minimized/closed |
| **Projects** | Save / open the real `.pkt` (`pt_save_project` / `pt_open_project`) | Persist the running topology, not just the plan JSON |
| **Export** | Plans, JS scripts, CLI configs | Reusable project files on disk |

👉 Full tool reference, device catalog, networking guides and architecture live in the **[documentation site](https://mats2208.github.io/MCP-Packet-Tracer/)**.

## Installation

**1. Install the server**

```bash
git clone https://github.com/Arminfx7/mcp-packet-tracer-configurado
cd mcp-packet-tracer-configurado
python -m venv .venv
# Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -e .
```

**2. Conecta tu cliente de chat**

En ChatGPT/Codex o en otro cliente de chat compatible con MCP, registra el servidor local con esta configuración:

```json
{
  "mcpServers": {
    "packet-tracer": {
      "command": "C:/ruta/al/repositorio/.venv/Scripts/python.exe",
      "args": ["-m", "packet_tracer_mcp", "--stdio"],
      "cwd": "C:/ruta/al/repositorio"
    }
  }
}
```

En Linux/macOS usa `.venv/bin/python`. La ruta debe apuntar a la carpeta donde clonaste este repositorio.

**3. Install the live-deploy extension** — _only if you want real-time deploy into a running Packet Tracer_

Download **`V5.pts`** from [**Releases**](https://github.com/Mats2208/MCP-Packet-Tracer/releases/latest), then in Packet Tracer go to **Extensions → Scripting → Configure PT Script Modules → Add…** and select it. Full walkthrough in [Live deploy](#live-deploy) below.

> **v0.6.0+ requires V5.** The bridge now authenticates with a per-machine token that the V5 extension reads automatically; builds before V5 can't authenticate.

**4. Usa el chat para solicitar la topología**

Ejemplo de prompt:

> Crea una topología RIP v2 con cinco routers en anillo, cinco switches y dos PCs por LAN. Usa las IP indicadas en el Excel, configura las interfaces, agrega etiquetas de IP y verifica con ping.

Consulta [`INSTALACION.md`](INSTALACION.md) para la configuración completa. Requiere **Python 3.11+**.

## Quick start

Just talk to your AI:

> *"Build a network with 2 routers, 2 switches, 4 PCs, DHCP and static routing."*

The LLM calls `pt_full_build`, which plans → validates → generates → deploys.
See the **[Quick Start guide](https://mats2208.github.io/MCP-Packet-Tracer/quickstart/)**.

## Live deploy

Stream topologies into a **running** Packet Tracer in real time. Install this repo's
own **MCP Control Center** extension once — the `.pts` from
[**Releases**](https://github.com/Mats2208/MCP-Packet-Tracer/releases/latest) — via
**Extensions → Scripting → Configure PT Script Modules → Add…**, then open
**Extensions → MCP BUILDER**. It auto-connects to the bridge — no snippet to paste.

📖 Full steps → **[Live Deploy Setup](https://mats2208.github.io/MCP-Packet-Tracer/live-deploy/)**.

## Credits & Acknowledgements

Live deploy runs through **our own Packet Tracer extension** — the **MCP Control
Center** (the `.pts` in [Releases](https://github.com/Mats2208/MCP-Packet-Tracer/releases/latest)).
Its Script-Engine helper layer was **inspired by**
**[PTBuilder](https://github.com/kimmknight/PTBuilder)** by
**Kim Knight ([@kimmknight](https://github.com/kimmknight))**, who pioneered driving
Packet Tracer's Script Engine from JavaScript — thanks for the groundwork. 🙏

> PTBuilder and Packet Tracer MCP are **separate, independent projects**. You install
> *our* extension, not PTBuilder. Full
> **[Credits & Attribution](https://mats2208.github.io/MCP-Packet-Tracer/credits/)**.

## Security

The live-deploy bridge requires a per-machine token as of **v0.6.0**. Earlier
versions had an unauthenticated bridge — any web page open while Packet Tracer
was running could execute code inside it. **Upgrade.**

Found a vulnerability? Report it privately via
[GitHub Security Advisories](https://github.com/Mats2208/MCP-Packet-Tracer/security/advisories/new),
not a public issue. [SECURITY.md](SECURITY.md) also documents the threat model —
worth reading before reporting, since some behaviour (like `pt_send_raw`
executing arbitrary JavaScript) is deliberate.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Tests run offline with
`python -m pytest`; no Packet Tracer needed.

## License

Released under the **[MIT License](LICENSE)** — © 2026 Mateo ([@Mats2208](https://github.com/Mats2208)).

<div align="center">

**Built with [MCP](https://modelcontextprotocol.io) · Powered by [Pydantic](https://docs.pydantic.dev) · Deploys to [Cisco Packet Tracer](https://www.netacad.com/) · Script-engine logic inspired by [PTBuilder](https://github.com/kimmknight/PTBuilder)**

If this project is useful to you, star it ⭐ and share it with the community.

</div>
