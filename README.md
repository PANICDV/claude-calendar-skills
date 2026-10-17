# Calendar planner skills

[Español](#español) · [English](#english)

---

## Español

Cuatro skills para Claude que convierten tus pendientes, tu rutina y tus compromisos en un
horario realista y lo entregan como archivos `.ics` para importar a Google Calendar, Apple
Calendar u Outlook. Los recordatorios recurrentes (pagos, limpiezas, mantenimientos) van
siempre en un calendario aparte.

### Las skills

| Skill | Idioma | Qué entrega |
|---|---|---|
| `planificador-calendario` | Español | El plan en **un solo calendario** (un color) y un calendario aparte de recordatorios recurrentes. |
| `planificador-calendario-secciones` | Español | **Un calendario por sección** (tesis, trabajo, trámites, rutina...), cada uno con su color, para reconocer cada tema de un vistazo y ocultarlo o mostrarlo con un clic. Los recordatorios van en su propio calendario. |
| `calendar-planner` | Inglés | Lo mismo que `planificador-calendario`, en inglés. |
| `calendar-planner-sections` | Inglés | Lo mismo que `planificador-calendario-secciones`, en inglés. |

Todas sirven para horarios diarios, semanales, trimestrales o de cualquier periodo, y
también para reajustar un plan ya entregado. Usa la versión normal si te basta con un
color, y la de secciones si quieres separar por categorías o colores (Google Calendar
ignora el color de cada evento dentro de un `.ics`, así que el color tiene que venir del
calendario).

Cada skill es una carpeta autocontenida dentro de `skills/`:

```
skills/<skill>/
├── SKILL.md       instrucciones para Claude
├── references/    cuestionario, formato del plan, cómo importar...
└── scripts/       build_ics.py (y build_sections.py en las de secciones)
```

### Instalación

**En claude.ai**

1. Comprime la carpeta de la skill en un `.zip`, de modo que la carpeta quede en la raíz
   del zip (por ejemplo `planificador-calendario.zip` → `planificador-calendario/SKILL.md`).
2. En claude.ai, ve a **Configuración → Capacidades → Skills** y sube el zip.
3. Repite con cada skill que quieras usar.

**En Claude Code**

Copia la carpeta de la skill a `~/.claude/skills/`:

```sh
cp -r skills/planificador-calendario ~/.claude/skills/
```

En Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\planificador-calendario "$env:USERPROFILE\.claude\skills\"
```

Los scripts necesitan Python 3.9 o superior. `python-dateutil` es recomendable (sin él, los
eventos repetitivos no se expanden al comprobar choques) y en Windows hace falta `tzdata`:

```sh
pip install -r requirements.txt
```

### Desarrollo y tests

`shared/` contiene la única fuente de `build_ics.py` y `build_sections.py`. Después de
editarlos, cópialos a cada skill con:

```sh
sh sync_scripts.sh
```

Para ejecutar los tests desde la raíz del repo:

```sh
pip install -r requirements-dev.txt
python -m pytest -q
```

Los tests también comprueban que las copias de cada skill coinciden con `shared/`.

**`tests/private_words.txt` (opcional y local).** Si existe, el test
`test_no_personal_data_in_skills` comprueba que ninguna skill contenga esas palabras. Es
una lista de expresiones regulares, una por línea, sin distinguir mayúsculas; las líneas
que empiezan por `#` son comentarios. El archivo está en `.gitignore` y nunca se sube al
repo, porque contiene datos personales. Si no existe, ese test se salta con un aviso.

---

## English

Four Claude skills that turn your to-dos, routine and commitments into a realistic
schedule and deliver it as `.ics` files to import into Google Calendar, Apple Calendar or
Outlook. Recurring reminders (bills, cleaning, maintenance) always go in a separate
calendar.

### The skills

| Skill | Language | What it delivers |
|---|---|---|
| `planificador-calendario` | Spanish | The plan as **a single calendar** (one color), plus a separate calendar of recurring reminders. |
| `planificador-calendario-secciones` | Spanish | **One calendar per section** (thesis, work, errands, routine...), each with its own color, so every topic is recognizable at a glance and can be hidden or shown with one click. Reminders go in their own calendar. |
| `calendar-planner` | English | Same as `planificador-calendario`, in English. |
| `calendar-planner-sections` | English | Same as `planificador-calendario-secciones`, in English. |

All of them handle daily, weekly, quarterly or any-length schedules, and can also
rebalance a plan already delivered. Use the regular version if one color is enough, and
the sections version to split by category or color (Google Calendar ignores per-event
colors inside an `.ics`, so the color has to come from the calendar).

Each skill is a self-contained folder under `skills/`:

```
skills/<skill>/
├── SKILL.md       instructions for Claude
├── references/    questionnaire, plan format, how to import...
└── scripts/       build_ics.py (plus build_sections.py in the sections skills)
```

### Installation

**On claude.ai**

1. Zip the skill folder so the folder sits at the root of the zip (for example
   `calendar-planner.zip` → `calendar-planner/SKILL.md`).
2. On claude.ai, go to **Settings → Capabilities → Skills** and upload the zip.
3. Repeat for each skill you want to use.

**In Claude Code**

Copy the skill folder to `~/.claude/skills/`:

```sh
cp -r skills/calendar-planner ~/.claude/skills/
```

On Windows (PowerShell):

```powershell
Copy-Item -Recurse skills\calendar-planner "$env:USERPROFILE\.claude\skills\"
```

The scripts need Python 3.9 or later. `python-dateutil` is recommended (without it,
recurring events are not expanded when checking for clashes), and Windows needs `tzdata`:

```sh
pip install -r requirements.txt
```

### Development and tests

`shared/` holds the single source of `build_ics.py` and `build_sections.py`. After editing
them, copy them into every skill with:

```sh
sh sync_scripts.sh
```

To run the tests from the repository root:

```sh
pip install -r requirements-dev.txt
python -m pytest -q
```

The tests also check that each skill's copies match `shared/`.

**`tests/private_words.txt` (optional and local).** If it exists, the
`test_no_personal_data_in_skills` test checks that no skill contains those words. It is a
list of regular expressions, one per line, case-insensitive; lines starting with `#` are
comments. The file is in `.gitignore` and is never committed, because it holds personal
data. If it is missing, that test is skipped with a notice.

---

## Licencia / License

[MIT](LICENSE) © 2026 Luis Camacho Urbina
