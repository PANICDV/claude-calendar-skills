# Formato de la especificación (spec JSON)

`scripts/build_ics.py` lee un JSON y genera un .ics. Escribe un JSON por archivo de salida
(uno para el plan y otro para los recordatorios).

Las rutas de los ejemplos son las de claude.ai (`/mnt/user-data/outputs/`). En otro entorno,
usa su carpeta de salida; el script crea la carpeta si no existe.

## Estructura

```json
{
  "calendar_name": "Plan 3–11 oct",
  "timezone": "America/Lima",
  "output": "/mnt/user-data/outputs/plan_3-11_oct.ics",
  "range_end": "2026-10-11",
  "color": "#33B679",
  "events": [ ... ]
}
```

| Campo | Obligatorio | Notas |
|---|---|---|
| `calendar_name` | sí | Nombre sugerido del calendario al importar. |
| `timezone` | sí | Zona IANA (`America/Lima`, `America/Mexico_City`, `Europe/Madrid`…). El script genera el VTIMEZONE con los cambios de horario reales y, si la zona tiene horario de verano, con su regla anual, así que los recordatorios sin fin siguen bien en años futuros. |
| `output` | sí | Ruta del .ics. |
| `range_end` | no | Último día del plan; mejora la validación de choques en los repetitivos. |
| `color` | no | Hex `#RRGGBB`. Lo respeta Apple; Google lo ignora (ahí el color se elige por calendario). |
| `lang` | no | Idioma de los mensajes del script: `es` (por defecto) o `en`. |

## Eventos con hora

```json
{"title": "🎓 Tesis: diapositivas (bloque 1)",
 "start": "2026-10-03T10:00", "end": "2026-10-03T12:30",
 "description": "Estructura completa y primeras secciones.",
 "alarm_min": 10}
```

Las horas son **locales, sin zona** (`2026-10-03T10:00`, sin `Z` ni `-05:00`): la zona la da
`timezone`. Un evento puede cruzar la medianoche (por ejemplo, el sueño):
`"start": "2026-10-02T23:00", "end": "2026-10-03T07:00"`.

## Eventos de todo el día

```json
{"title": "💡 Pagar la luz", "date": "2026-11-03"}
```
Para varios días: agrega `"end_date": "2026-11-05"` (inclusive). No llevan hora, así que no
entran en la validación de choques.

## Repetición (`repeat`)

| Necesidad | `repeat` |
|---|---|
| Todos los días hasta el 11/10 | `{"freq": "DAILY", "until": "2026-10-11"}` |
| Lunes a viernes | `{"freq": "WEEKLY", "byday": ["MO","TU","WE","TH","FR"], "until": "2026-10-09"}` |
| Cada 30 días | `{"freq": "DAILY", "interval": 30}` |
| El 3 de cada mes | `{"freq": "MONTHLY", "bymonthday": 3}` |
| Último día de cada mes | `{"freq": "MONTHLY", "bymonthday": -1}` |
| Cada 2 semanas el sábado | `{"freq": "WEEKLY", "interval": 2, "byday": ["SA"]}` |
| Una vez al año (15 de marzo) | `{"freq": "YEARLY", "bymonth": 3, "bymonthday": 15}` |
| 6 repeticiones | agrega `"count": 6` |
| Regla libre | `{"rrule": "FREQ=MONTHLY;BYDAY=1MO"}` (primer lunes del mes) |

`until` es una fecha local **inclusiva**. Sin `until` ni `count`, la repetición es indefinida,
que es lo correcto para los recordatorios permanentes. El script escribe el `UNTIL` en el
formato que exige el estándar (fecha en los eventos de todo el día, hora UTC en los demás),
también cuando viene dentro de una regla libre.

## Otros campos
- `alarm_min`: minutos de aviso antes del inicio.
- `location`: lugar.
- `allow_overlap: true`: el script no reporta choques de este evento (útil para un evento-aviso que se superpone a propósito).
- `uid`: opcional; si no se da, se genera uno estable a partir del título y la fecha. Si dos eventos tienen el mismo título e inicio, el script avisa y les da UID distintos.

## Ejemplo: recordatorios

```json
{
  "calendar_name": "🔔 Recordatorios",
  "timezone": "America/Lima",
  "output": "/mnt/user-data/outputs/recordatorios.ics",
  "events": [
    {"title": "💡 Pagar la luz", "date": "2026-11-03", "repeat": {"freq": "MONTHLY", "bymonthday": 3}},
    {"title": "🔔 Mañana: pagar la luz", "date": "2026-11-02", "repeat": {"freq": "MONTHLY", "bymonthday": 2}},
    {"title": "🧊 Limpiar el refrigerador", "start": "2026-10-10T10:00", "end": "2026-10-10T10:45",
     "repeat": {"freq": "DAILY", "interval": 30}, "alarm_min": 30}
  ]
}
```

## Salida del script
```
✅ Sin choques entre eventos con hora.
Horas por categoría (incluye repeticiones):
   🎓     20.0 h
   🖥     13.8 h
   ...
📄 /mnt/user-data/outputs/plan_3-11_oct.ics  (73 eventos)
```
- **Choques**: corrígelos en el JSON y vuelve a ejecutar.
- **Errores de formato** (zona desconocida, fecha inválida, fin antes del inicio, `freq` o `byday` mal escritos): el script los lista todos de una vez y no escribe el archivo.
- **Falta python-dateutil**: el script lo avisa; instálalo, porque sin él no se validan los eventos repetitivos.

Con `--check` solo valida, sin escribir el archivo.
