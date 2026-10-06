# Créditos y procedencia

Esta copia se publica para documentar el trabajo realizado con Cisco Packet Tracer y el MCP.

## Proyecto base

- Código base: [Mats2208/MCP-Packet-Tracer](https://github.com/Mats2208/MCP-Packet-Tracer).
- Autor y mantenedor del proyecto base: Mateo ([Mats2208](https://github.com/Mats2208)).
- Licencia heredada: MIT, según el archivo `LICENSE` incluido en este repositorio.

## Referencias técnicas

- [Model Context Protocol](https://modelcontextprotocol.io) y el SDK de Python usado por el servidor.
- [Pydantic](https://docs.pydantic.dev) para modelos y validación.
- [Cisco Packet Tracer](https://www.netacad.com/cisco-packet-tracer) como simulador de red.
- [Packet Tracer IPC API](https://tutorials.ptnetacad.net/help/default/IpcAPI/) como referencia de la interfaz de automatización.
- [PTBuilder](https://github.com/kimmknight/PTBuilder), de Kim Knight, como referencia histórica para helpers del Script Engine. PTBuilder es un proyecto independiente y no forma parte de este MCP.

## Trabajo añadido en esta copia

- Topología educativa RIP v2 con cinco routers, cinco LAN, enlaces seriales /30 y etiquetas de IP.
- Topología de subneteo anterior exportada como proyecto `.pkt`.
- Parámetros `lan_base` y `link_base` en las herramientas de planificación para seleccionar las redes LAN y los enlaces entre routers.
- Instrucciones de instalación y scripts portables para pruebas y consulta de herramientas.

Los archivos y configuraciones de Packet Tracer incluidos aquí son material educativo creado para este laboratorio.
