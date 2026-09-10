# Streamlit-App auf Heroku deployen

Dieser Ordner enthält alles, was Heroku für den Build braucht:

| Datei                    | Zweck                                                          |
| ------------------------ | -------------------------------------------------------------- |
| `app.py`                 | die Streamlit-App                                               |
| `Procfile`               | Startbefehl; bindet Streamlit an `$PORT` und `0.0.0.0`          |
| `requirements.txt`       | Abhängigkeiten (gepinnt auf die Versionen aus dem Buch)         |
| `.python-version`        | Python-Version des Buildpacks                                   |
| `.streamlit/config.toml` | Server läuft headless, keine Usage-Statistiken                  |

## 1. App anlegen

```bash
heroku login
heroku create meine-debatten-app
```

## 2. API-Schlüssel als Config Var setzen

Die `.env`-Datei wird **nicht** mit deployt. Der Schlüssel kommt auf Heroku aus
den Config Vars:

```bash
heroku config:set OPENAI_API_KEY=sk-... --app meine-debatten-app
# optional, sonst wird gpt-5.6-luna verwendet
heroku config:set OPENAI_MODEL=gpt-5.6-luna --app meine-debatten-app
```

## 3. Deployen

Heroku erwartet `Procfile` und `requirements.txt` im Wurzelverzeichnis des
gepushten Repositorys. Es gibt zwei Wege:

**Variante A – eigenes Repository für diesen Ordner (am einfachsten):**

```bash
cd Code/11_Deployment/heroku
git init
git add .
git commit -m "Streamlit-App für Heroku"
heroku git:remote --app meine-debatten-app
git push heroku main
```

**Variante B – Unterordner aus dem Buch-Repository pushen:**

```bash
# im Wurzelverzeichnis des Buch-Repositorys
heroku git:remote --app meine-debatten-app
git subtree push --prefix Code/11_Deployment/heroku heroku main
```

## 4. App öffnen

```bash
heroku open --app meine-debatten-app
heroku logs --tail --app meine-debatten-app   # bei Problemen
```

## Hinweise

- Läuft die App nach dem Deployment in einen Timeout, liegt es meist an der
  30-Sekunden-Grenze des Heroku-Routers: Bei vielen Runden dauert die Debatte
  länger als die erste Antwort des Servers. Der Websocket von Streamlit ist
  davon nicht betroffen, der initiale Seitenaufruf schon – ein `basic`-Dyno
  statt `eco` hilft gegen das langsame Aufwachen.
- Bei mehreren Dynos gibt es keine gemeinsame Session – Streamlit hält den
  Zustand pro Prozess. Für diese App ist das unkritisch.
