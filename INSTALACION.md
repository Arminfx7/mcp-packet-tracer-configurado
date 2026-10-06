# Instalación y uso

## Requisitos

- Python 3.11 o superior.
- Cisco Packet Tracer instalado para abrir los archivos `.pkt`.
- Un cliente MCP compatible, por ejemplo Claude Desktop, VS Code/Copilot o Codex.

## Instalación local

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

En Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

## Ejecutar el servidor MCP

```bash
pt-mcp --stdio
```

También se puede ejecutar con:

```bash
python -m packet_tracer_mcp --stdio
```

## Configuración del cliente MCP

Usa la ruta absoluta de tu copia local y el intérprete del entorno virtual. Ejemplo para un cliente que acepta JSON:

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

En Linux/macOS cambia `Scripts/python.exe` por `.venv/bin/python`.

## Proyectos incluidos

Abre estos archivos desde Cisco Packet Tracer:

- `projects/topologia_RIP_5_routers.pkt`: anillo de cinco routers con RIP v2, cinco LAN y dos PCs por LAN.
- `projects/topologia_excel_tipoA_tipoB.pkt`: topología anterior con direccionamiento basado en el ejercicio de subneteo.

Las etiquetas de los dispositivos muestran únicamente las IP utilizadas. Después de abrir un proyecto puedes comprobar la conectividad con `ping` entre PCs de LAN diferentes.

## Pruebas

```bash
pytest
```

Los scripts de `scripts/` usan rutas relativas al repositorio y no dependen de la carpeta donde fue creado originalmente.

## Seguridad

No subas tokens, contraseñas, archivos `.env`, credenciales de Packet Tracer ni configuraciones privadas. El repositorio de referencia contiene el código del MCP; los proyectos `.pkt` de esta copia son configuraciones educativas.
