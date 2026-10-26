---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Certificación de operativa ante prop firms]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/prop-firms/que-no-te-nieguen-el-pago-como-certificar-tu-operativa-ante-una-prop-firm"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Certificación de operativa ante prop firms

## Síntesis vigente

Propuesta de preservar evidencia de código, configuración y ejecución anterior a las operaciones. Su propio artículo aclara que no garantiza cobro ni reemplaza las reglas de cada firma.

## Conocimiento extraído

El post adjunta un PDF de cinco páginas, una versión HTML y un RAR con script. La vista previa del PDF en Chrome permite recuperar el protocolo:

1. Carpeta por cuenta con `.sqx`, código exportado, `.set`, reglas de riesgo, broker/servidor/símbolo y mapeo EA↔magic↔terminal.
2. Magic único y comentario de orden para relacionar operaciones con la EA sellada.
3. Sellar antes de operar y antes de cada cambio; repetir periódicamente aunque no haya cambios.
4. Guardar proyecto SQX y evidencia de construcción, no solo el EA final.
5. Revisar coberturas incompatibles entre cuentas, exportar statements, registrar desvíos con fecha y motivo y mantener respaldo separado.

Herramientas descritas: Python con hash SHA-256 y manifiesto, sello temporal FreeTSA RFC 3161, opcional OpenTimestamps y Git firmado. La huella se envía al servicio de timestamp; el autor dice no enviar archivos. **No se ejecutó el script ni se transmitió información de Rodrigo.**

El expediente propone aportar verificación independiente de que un contenido ya existía, junto a trazabilidad y reglas de riesgo. No demuestra por sí solo cumplimiento de condiciones de una prop ni autoría original del código.

## Comentarios y matices

Cristobal y José dudan que evidencia técnica baste ante una denegación discrecional; Ricardo la considera defensa preventiva. Otro miembro comparte un conflicto de pago y confidencialidad. Son testimonios no investigados; no se toman acusaciones como hechos verificados.

## Adjuntos y cobertura

Post y nueve comentarios revisados en Chrome; PDF de cinco páginas revisado inicialmente en la vista previa y después leído íntegramente como texto local por autorización de Rodrigo. Adjuntos: Articulo_certificacion_operativa.pdf, sellar_operativa.rar y Articulo_certificacion_operativa.html. No se ejecutó ni extrajo el RAR.

## Interés para Forge

Prioridad de consulta: **Media**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/prop-firms/que-no-te-nieguen-el-pago-como-certificar-tu-operativa-ante-una-prop-firm).
- Autor: Ricardo Exequiel Esposito Laine. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Certificación de operativa ante prop firms]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Archivos complementarios recibidos

- `Articulo_certificacion_operativa.html`: versión alternativa del artículo, inspeccionada como texto sin ejecutar scripts ni cargar recursos externos.
- `sellar_operativa.rar`: archivo recibido e inventariado; no se ejecutó. No hay extractor RAR disponible en esta sesión, por lo que el script completo permanece sin inspección y no debe considerarse auditado.
- El pseudocódigo del PDF calcula huellas, manifiesto y petición TSA, pero el ejemplo no constituye una verificación completa del certificado, su cadena ni la autoría de los archivos.

## Límites y contradicciones

El artículo declara que no cubre el pasado anterior al primer sello, no legitima una infracción y no garantiza pago. La afirmación de invertir la carga de prueba es opinión del autor, no conclusión jurídica. No se auditó criptografía, validez del TSA ni el contenido ejecutable.
