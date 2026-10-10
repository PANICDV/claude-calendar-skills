---
name: planificador-calendario
description: Diseña horarios optimizados (diarios, semanales, por periodos cortos o largos, trimestrales) y los entrega como archivos .ics para importar a Google Calendar, Apple Calendar u Outlook, más un calendario aparte de recordatorios recurrentes (pagos, limpiezas, mantenimientos). Usar SIEMPRE que la persona quiera organizarse, planificar su semana/mes, distribuir pendientes o tareas en el tiempo, armar o respetar una rutina, crear recordatorios que se repiten (cada N días, cada día X del mes) o pida un archivo para importar a su calendario, aunque no mencione ".ics" ni "skill". También para actualizar o reajustar un plan ya entregado. Esta versión entrega el plan en un solo calendario (un color).
---

# Planificador de calendario

Convierte los pendientes, la rutina y los compromisos de una persona en un horario
realista y optimizado, y lo entrega como archivos que se importan al calendario.

Hay dos productos y casi siempre van separados, porque cumplen funciones distintas:

| Archivo | Qué contiene | Por qué separado |
|---|---|---|
| `plan_<periodo>.ics` | Rutina fija + tareas distribuidas en bloques | Se reemplaza cada vez que el plan se actualiza |
| `recordatorios.ics` | Pagos, limpiezas, mantenimientos que se repiten | Es permanente; se superpone al calendario normal y no se toca al actualizar el plan |

Modos de uso:
- **Plan completo**: rutina + pendientes (+ recordatorios si los hay).
- **Solo recordatorios**: la persona solo quiere avisos recurrentes (ej. "cada 30 días limpiar el refrigerador", "el 3 de cada mes pagar la luz").
- **Actualizar plan**: ya hay un plan entregado y hay que reajustarlo (ver "Actualizaciones").

## Flujo de trabajo

### 1. Reunir lo que ya se sabe
Antes de preguntar nada, revisa la conversación y la memoria disponible: horas de sueño,
horario laboral, traslados, hijos, mascotas, preferencias de planificación. Lo que ya
conoces no se vuelve a preguntar; se confirma en una línea ("Tomo tu rutina de siempre:
duermes 23:00–7:00, trabajas L–V de 9:00 a 18:00, recoges a los niños a las 15:30… ¿sigue igual?"). Preguntar de nuevo
algo que la persona ya dijo transmite que no se la escuchó.

### 2. Entrevista por bloques
Si falta información, pregunta **por bloques en forma de lista numerada**, un bloque por
mensaje, para que la persona responda rápido por número. Los bloques y sus preguntas están
en `references/cuestionario.md`; léelo antes de preguntar.

- Salta los bloques que no aplican (modo "solo recordatorios" → bloques 1 y 4).
- Si la persona ya volcó todo en un mensaje, pregunta solo lo que falte, en un único bloque.
- Acepta respuestas parciales: lo que no sepa (duraciones, energía) lo estimas tú y lo dices.
- No más de 3–4 rondas. Con lo esencial (periodo, sueño, compromisos fijos, pendientes) ya se puede diseñar; lo demás se ajusta después.

### 3. Diseñar el horario
Aplica los principios de la sección siguiente. Trabaja en este orden:
1. **Anclas fijas**: sueño, trabajo, traslados, comidas, cuidado de hijos/mascotas, compromisos con hora.
2. **Tareas con fecha o con horario hábil** (bancos, llamadas, oficinas, trámites).
3. **Proyectos grandes** divididos en bloques.
4. **Tareas pequeñas** agrupadas en huecos cortos.
5. **Espacios flexibles** y tiempo libre.

### 4. Generar y validar los archivos
Escribe una especificación JSON y ejecuta el script (formato completo en
`references/formato_spec.md`):

```bash
python <ruta-skill>/scripts/build_ics.py <carpeta-de-trabajo>/spec_plan.json
```

El script valida el JSON (si hay errores, los lista todos y no escribe nada), genera el .ics,
detecta **choques** entre eventos (expandiendo los repetitivos) e imprime **horas por
categoría**. Corrige todo choque no intencional antes de entregar, y usa el resumen de horas
para comprobar que las prioridades reciben el tiempo que la persona pidió. Si avisa que falta
`python-dateutil`, instálalo (`pip install python-dateutil`) y vuelve a ejecutar: sin esa
librería no se validan los eventos repetitivos.

Guarda los archivos en la carpeta de salida del entorno (en claude.ai: `/mnt/user-data/outputs/`;
el script crea la carpeta si no existe) y entrégalos con la herramienta del entorno para
compartir archivos (en claude.ai: `present_files`).

### 5. Entregar
Mensaje breve en el idioma de la persona:
- Tabla corta con la rutina diaria (hora → actividad).
- En prosa, las 3–6 decisiones clave (qué se priorizó, dónde quedan los trámites, qué días son más ligeros).
- Cualquier supuesto que tomaste ("puse a Toby 30 min porque asumí que es un perro; si no, dime").
- Instrucciones de importación (ver `references/importar.md`): **siempre en un calendario nuevo, nunca en el principal**.

## Principios de diseño

Cada principio tiene un porqué; úsalos con criterio, no como reglas ciegas.

- **El sueño es un evento visible.** Si no aparece en el calendario, el plan se lo come. Respeta las horas que la persona indique y deja ~30 min entre despertar y la primera actividad exigente.
- **Trabajo profundo en las horas de más energía.** Pregunta cuáles son; si no lo sabe, usa la mañana. Lo mecánico (correos, trámites cortos) va en horas de menor energía.
- **Trámites en horario hábil.** Bancos, llamadas, clínicas y oficinas: L–V aprox. 9:00–18:00, sábados por la mañana. Pon antes un bloque de preparación de documentos si el trámite lo necesita.
- **Bloques de tamaño útil.** Trabajo profundo: 60–150 min. Tareas pequeñas: 15–45 min, agrupadas. Menos de 45 min no alcanza para concentrarse en algo complejo; más de 2,5 h seguidas rinde poco.
- **Variedad diaria.** Ningún día dedicado a un solo tema; máximo ~2 bloques del mismo tema por día, separados por otra cosa. Alterna lo exigente con lo liviano.
- **Proyectos grandes en bloques numerados.** "Tesis: diapositivas (bloque 3)". En la descripción pon el objetivo concreto del bloque. Pon el bloque de cierre ("TERMINAR …") con margen antes de la fecha límite.
- **Fechas inciertas → opción A / opción B.** Si un trámite puede caer en dos días, reserva un bloque en cada uno y escribe en la descripción que el que no se use se convierte en tiempo para el tema prioritario. Así no se pierde tiempo ni se sobrecarga el plan.
- **Espacios flexibles 🔄.** Aproximadamente uno por día (10–15 % del tiempo disponible), para mover lo que no se cumplió. Un plan sin holgura se rompe al primer imprevisto y la persona lo abandona.
- **Márgenes tras eventos variables.** Si el almuerzo a veces se alarga 15 min, el siguiente bloque empieza 15 min después.
- **No llenar hasta la hora de dormir.** Deja tiempo libre o familiar al final del día y días más ligeros (por ejemplo, viernes por la noche y parte del domingo).
- **Revisión semanal.** Un bloque corto para revisar avances y pedir el ajuste del plan, y otro para planificar la semana siguiente.
- **Prioridades explícitas mandan.** Si la persona dice "dale más a X", reasigna tiempo desde lo menos urgente y muestra una tabla antes/después de horas por tema.
- **Alarmas solo en lo crítico.** Citas, trámites con hora, pagos, votaciones, recojo de hijos. Si todo suena, nada suena.

### Según el horizonte
| Tipo | Cómo planificar |
|---|---|
| Diaria | Bloques detallados de toda la jornada. |
| Semanal / periodo corto (≤ 3 semanas) | Detalle completo día por día. |
| Periodo largo / trimestral | Detalle fino solo para las primeras 1–2 semanas. Después: rutina recurrente + hitos semanales por proyecto ("Semana 5: informe listo") + revisiones semanales. Los planes detallados a largo plazo caducan rápido, así que es mejor revisarlos y ajustarlos cada semana. |

## Formato de los eventos

- **Rutina como eventos repetitivos** (`repeat`), no como copias: es más limpio y más fácil de borrar.
- **Título**: emoji + tema + detalle. El emoji sirve para reconocer la categoría y para buscar (borrar o filtrar) en el calendario. Usa el mismo emoji para el mismo tema durante todo el plan.

| Emoji | Uso típico |
|---|---|
| 😴 🏃 🍳 🍽️ | Sueño, ejercicio, comidas |
| 🐕 🎒 🧹 | Mascotas, hijos/colegio, limpieza |
| 🎓 🎤 | Estudios, tesis, ensayos/presentaciones |
| 🖥️ 🤖 🧩 | Tecnología, proyectos técnicos, herramientas |
| 🏦 💳 📄 🚗 📞 | Bancos, pagos, documentos, vehículo, llamadas |
| 🗂️ 📧 🎨 📋 | Organización, correo, diseño, revisión o planificación |
| 📈 💾 | Inversiones/mercado, ventas |
| 🔄 | Espacio flexible |

- **Descripción**: el objetivo concreto, la alternativa si la hay y los datos útiles (nombre del médico, qué documentos llevar).

## Recordatorios recurrentes

Van en `recordatorios.ics`, con un `calendar_name` propio (por ejemplo "🔔 Recordatorios").
- Pagos: evento de todo el día en la fecha de pago. Si piden aviso previo, agrega un segundo evento el día anterior, porque las alarmas de eventos de todo el día se comportan distinto según la app.
- "Cada N días": `freq DAILY` + `interval N`. "Día X de cada mes": `freq MONTHLY` + `bymonthday X`. Para fin de mes usa `bymonthday -1`. Si X es 29–31, avisa que los meses cortos se saltan ese día y ofrece usar el último día del mes.
- Sin fecha de fin, salvo que la persona la dé: los recordatorios son permanentes.
- Las tareas de mantenimiento (limpiar el refrigerador) pueden llevar hora sugerida en un hueco típico de la rutina de la persona.

## Actualizaciones

Cuando la persona pide cambios ("dale más tiempo a X", "el martes no puedo"):
- Conserva todo lo que no pidió cambiar: rutina, decisiones previas, emojis.
- Cambia solo lo pedido y reequilibra lo mínimo necesario.
- Versiona el archivo (`plan_…_v2.ics`) y recuerda: **borrar el calendario del plan anterior y crear uno nuevo antes de importar**, porque Google Calendar no reemplaza de forma fiable los eventos ya importados y quedarían duplicados.
- El calendario de recordatorios no se toca, salvo que los cambios sean sobre recordatorios.
- Si la persona dice que algo de tu plan le gustó, aplícalo también en las proyecciones futuras.

## Archivos de referencia
- `references/cuestionario.md`: bloques de preguntas para la entrevista. Léelo antes de preguntar.
- `references/formato_spec.md`: formato del JSON que lee el script, con ejemplos.
- `references/importar.md`: cómo importar y borrar en Google, Apple y Outlook.
