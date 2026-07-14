# A walk-through of how to set up online experiments on yeslab-survey website

## Step 1: prepare your experiment

### Design your experiment

#### 1. PsychoPy

You may use PsychoPy Builder to design your experiment. To host it on yeslab-survey (instead of Pavlovia), you need a local `lib/` folder containing the PsychoJS runtime, plus your compiled HTML/JS.

**How to get `lib/` and the web files**

**Option 1 — Export from PsychoPy Builder**

1. Open your `.psyexp` in PsychoPy Builder.
2. In **Experiment Settings → Online**, set **Output path** to blank (files go in the experiment folder) and set **Export HTML** to **on save** or **manually**.
3. Generate the browser version:
   - **File → Export HTML**, or
   - **Run → Run JS for local debug** (globe/bug icon in the Runner).
4. PsychoPy creates:
   - `index.html`
   - `[your_experiment].js` (the PsychoJS task script)
   - `lib/` with PsychoJS files (e.g. `psychojs-YYYY.X.X.js`, `.iife.js`, `.css`)
5. Copy `lib/` into the same folder as `index.html` if it was created elsewhere. Upload this whole folder to the server later — Pavlovia will not provide `lib/` for you when self-hosting.

**Option 2 — Download `lib/` directly from Pavlovia (version-specific)**

You can curl the PsychoJS runtime from `https://lib.pavlovia.org/`. **This is version-specific** — the filenames must match the PsychoJS version your experiment expects (check `index.html` / `[task].js` imports, e.g. `2021.2.3`). Mixing versions will break loading.

```bash
mkdir -p lib && cd lib
for f in psychojs-2021.2.3.js psychojs-2021.2.3.css psychojs-2021.2.3.iife.js; do
  curl -fL --retry 3 -O "https://lib.pavlovia.org/$f"
done
```

Replace `2021.2.3` with your experiment’s PsychoJS version.


#### 2. jsPsych

1. Create an HTML page that loads jsPsych from a CDN or a local copy, e.g.:
   ```html
   <script src="https://unpkg.com/jspsych@7.3.4"></script>
   <script src="https://unpkg.com/@jspsych/plugin-html-keyboard-response@1.1.2"></script>
   ```
2. Build your timeline with `initJsPsych({ on_finish: ... })`.
3. On finish, `POST` trial data as JSON to `save_data.php` (see below). You can keep everything in one file (e.g. `experiment.html`) or split HTML + JS.

---

### Set up data saving pipeline

Both frameworks use the same server pieces:

- `save_data.php` — receives a POST and writes a CSV under `data/`
- `data/` — must exist and be writable by the web server
- `data/.htaccess` — blocks direct browser access to saved CSVs
- `test_server_config.php` / `test_save_data.html` — verify PHP and saving before real runs

For sample files, copy from:
- PsychoPy: [yeslab-survey_setup_sample/psychopy/](yeslab-survey_setup_sample/psychopy)
- jsPsych: [yeslab-survey_setup_sample/jspsych/](yeslab-survey_setup_sample/jspsych)

### Configurate your experiment

#### Pattern A — PsychoPy / PsychoJS (CSV string)

JS builds a CSV string and sends:

```json
{ "filename": "PID_task_yyyy-mm-dd.csv", "data": "<csv string>" }
```

`save_data.php` validates the filename and writes `data/<filename>`.

Copy [yeslab-survey_setup_sample/psychopy/](yeslab-survey_setup_sample/psychopy) into your experiment folder. In an exit routine (JS code component), disable Pavlovia-style download and POST instead, e.g. set `psychoJS._saveResults = 0` and call your save function (as in the trait task).

#### Pattern B — jsPsych (JSON trial array)

JS sends an **array of trial objects**:

```js
fetch('save_data.php', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(jsPsych.data.get().values()),
});
```

`save_data.php` then:

1. Decodes the JSON array
2. Requires a `participant_id` field on the rows
3. Builds ordered CSV headers
4. Writes `data/participant_<id>_<timestamp>_v<version>.csv`

Copy [yeslab-survey_setup_sample/jspsych/](yeslab-survey_setup_sample/jspsych) into your experiment folder, then adjust the preferred column list in PHP to match your trial fields. In `on_finish`, call `jsPsych.data.get().addToAll({ participant_id, ... })` before POSTing so every row has the ID.

**Guardrail:**

```bash
mkdir -p data
# data/.htaccess should deny web listing of CSVs (included in the sample folders)
```

### Local testing

Use Python’s static server to exercise the main experiment JS only. PHP save/testing is done later on yeslab-survey (Step 5).

```bash
cd [your experiment folder]
python -m http.server 8000
```

Open the experiment with the URL parameters your task expects, for example:
- PsychoPy (URL fields matched via `util.addInfoFromUrl`):  
  `http://localhost:8000/index.html?ResponseID=TEST&PROLIFIC_PID=TEST123`
- jsPsych + SONA (`?id=` survey code):  
  `http://localhost:8000/experiment.html?id=TEST001`

Do **not** open via `file://` (module scripts and relative asset paths will fail). Data saving will not work locally with this server — that is expected.

## Step 2 (Optional): Upload your experiment to GitHub

This step is optional, but highly recommended — it makes updating the design easier. Change locally, push to GitHub, then `git pull` on the survey server.

## Step 3: Log into yeslab-survey website

```bash
ssh web-yeslab-survey@jailhost.lscg.ucsb.edu
```

You can access the password [here](https://docs.google.com/document/d/1MhgXB1-aBgnXH2br9VX6TUkh15gLPT9Y-YHGGTotI_E/edit?usp=sharing).

## Step 4: Copy your experimental folder to yeslab-survey

**IMPORTANT:** Put all files under one folder named for your experiment under `~/public_html`, e.g. `~/public_html/my_experiment/`.

If the experiment is on GitHub, you can `git clone` directly into `~/public_html/`.

Make sure these are present (names vary by framework):

| Item | PsychoPy | jsPsych |
|------|----------|---------|
| Entry page | `index.html` | `experiment.html` (or `index.html`) |
| Task code | `[task].js` | often embedded in the HTML |
| PsychoJS runtime | `lib/` | not needed |
| Data backend | `save_data.php`, `data/.htaccess` | same |
| Tests | `test_server_config.php`, `test_save_data.html` | same |
| Stimuli / conditions | images, `.xlsx`, etc. | images, CSVs, etc. |

## Step 5: Change file r/w access and remote testing

**Change file access**

```bash
cd ~/public_html/[your experiment folder]
mkdir -p data
chmod 777 data/
chmod 644 *.html *.php *.js
```

(`chmod 777 data/` is needed on this server so the web process can write CSVs.)

**Remote testing**

1. Server config:  
   `https://yeslab-survey.psych.ucsb.edu/[your experiment folder]/test_server_config.php`  
   Confirm all checks pass.
2. Data saving:  
   `https://yeslab-survey.psych.ucsb.edu/[your experiment folder]/test_save_data.html`  
   Click **Test Save Data**, then confirm a CSV in `data/` on the server.

**You are ready to go!**🎉


## Troubleshooting

- **404 on `save_data.php`**: upload PHP files to the same directory as the experiment HTML
- **Data directory not writable**: `chmod 777 data/`
- **Experiment won't load (PsychoPy)**: confirm `lib/` exists next to `index.html` and that `index.html` points to your `[task].js`
- **Must use HTTP for local JS testing**: do not open via `file://`; use `python -m http.server 8000`
- **Save fails locally**: expected with the Python static server — test PHP saving on yeslab-survey with `test_server_config.php` / `test_save_data.html`
- **Save works in test HTML but not in the experiment**: payload shape mismatch — PsychoPy must send `{filename, data}`; jsPsych must send a JSON **array** with `participant_id` (Pattern A vs B above)
- Check `data/error.log` for PHP errors
