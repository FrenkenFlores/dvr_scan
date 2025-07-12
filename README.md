# DVR Scan



##

```bash

flask --app dvr_scan/ init-db
flask --app dvr_scan/ run -p 7777 --debug
```
## Final project fs

```

/home/user/Projects/dvr_scan
├── dvr_scan/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── ui.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── ui/
│   │       ├── camera.html
│   │       ├── logs.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_ui.py
├── .venv/
├── pyproject.toml
└── MANIFEST.in

```