# leaflink-online

[繁體中文](README_zh-Hant.md) | English

114-2 Web and Database course Project, inspired by Obsidian.

A simple web-based implementation of Obsidian's core features.

## Quick Start

> **Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and Docker Compose

1. Clone this repository.
2. Copy the example environment file and fill in your own secrets:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set `POSTGRES_PASSWORD` and `JWT_SECRET` to values of your choice.
3. Start all three services (database, backend, frontend) with a single command:
   ```bash
   docker compose up --build
   ```
4. Open your browser:

| Service      | URL                          |
| :----------: | :--------------------------- |
| Frontend     | http://localhost             |
| Backend docs | http://localhost:8000/docs   |

## Tech stack
### Frontend
Framework: SvelteKit\
Using Single-page app with HTML and CSS. Running on Nginx.

### Backend
FastAPI running on Docker container.

### Database
Using PostgreSQL.

### Others
Provides Dockerfile and Docker Compose for quickly setting up a demo.

## Development environment
### Frontend
We use [fnm](https://github.com/Schniz/fnm) to manage Node.js. (SvelteKit requires Node.js)\
Package management using `pnpm`.\
To develop the frontend, navigate into the `frontend` directory.\
Use the following commands for development:
|      Command      | Description                                                          |
| :---------------: | :------------------------------------------------------------------- |
| `pnpm dev --open` | Runs the dev Server and watches for changes. Press `Ctrl+C` to stop. |
> Note: Using `--open` will automatically open the app in a new browser tab.\
> If you don't want this behavior, remove the `--open` flag.

### Backend
|      Environment      | Description                                               |
| :-------------------: | :-------------------------------------------------------- |
|        Python         | 3.12+                                                     |
| Dependency Management | Astral uv                                                 |
|      Development      | `uvicorn main:app --reload`                               |
|      Production       | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app` |

Once the backend is running, interactive API documentation is available at:
|    Tools     | URL                                |
| :----------: | :--------------------------------- |
|  Swagger UI  | http://localhost:8000/docs         |
|    ReDoc     | http://localhost:8000/redoc        |
| OpenAPI JSON | http://localhost:8000/openapi.json |

### Project directory structure
```
leaflink-online
├── frontend/
├── backend/  
├── db/
└── README.md
```

## MVP
### Goal
- User features
  - [x] User registration
  - [x] Login + JWT
- [x] Vault privacy settings
- [x] Markdown notes CRUD and browsing
- [x] Markdown notes and vaults upload
- [x] `[[Bi-directional links]]` resolve and backlink display
- [x] Tags system and Full-text search (PostgreSQL tsvector)

### Additional targets
- [x] Personal online Markdown notes and vaults editing
- [ ] Knowledge network (D3.js)

## Database design
![](./docs/webFP.svg)

## Database Normalization Analysis

### 1NF (First Normal Form)

All tables satisfy the following:
- Each column stores an indivisible atomic value with no repeating groups
- Each table has a clearly defined primary key

**Result: All passed ✓**

### 2NF (Second Normal Form)

2NF requires the elimination of *partial functional dependencies* — every non-key attribute must be fully dependent on the entire primary key, not just part of a composite key.

The only table with a composite primary key is `note_tags(note_id, tag_id)`, which has no non-key attributes, so no partial dependencies exist. All other tables have single-column primary keys, so 2NF is satisfied automatically.

**Result: All passed ✓**

### 3NF (Third Normal Form)

3NF requires the elimination of *transitive dependencies* — no non-key attribute may indirectly depend on the primary key through another non-key attribute.

| Table       | Notes                                                                                                                  |
| :---------- | :--------------------------------------------------------------------------------------------------------------------- |
| `users`     | `username` and `email` are both `UNIQUE NOT NULL`, making them candidate keys; no transitive dependencies ✓           |
| `vaults`    | All attributes depend directly on `id`; no transitive dependencies ✓                                                  |
| `notes`     | All attributes depend directly on `id`; `search_vector` is a derived column (`GENERATED`) and does not introduce any dependency issues ✓ |
| `links`     | `(src_note, dest_note)` has a `UNIQUE` constraint, making it a candidate key; no transitive dependencies ✓            |
| `tags`      | `name` is `UNIQUE NOT NULL`, making it a candidate key; no transitive dependencies ✓                                  |
| `note_tags` | Has no non-key attributes; trivially satisfied ✓                                                                       |

**Result: All passed ✓**

### BCNF (Boyce-Codd Normal Form)

BCNF is a stricter standard than 3NF, requiring that every determinant must be a candidate key.

| Table       | Candidate Keys                | BCNF  |
| :---------- | :---------------------------- | :---: |
| `users`     | `id`, `username`, `email`     |   ✓   |
| `vaults`    | `id`                          |   ✓   |
| `notes`     | `id`                          |   ✓   |
| `links`     | `id`, `(src_note, dest_note)` |   ✓   |
| `tags`      | `id`, `name`                  |   ✓   |
| `note_tags` | `(note_id, tag_id)`           |   ✓   |

In every table, each determinant is a candidate key — no BCNF violations exist.

**Result: All passed ✓**

# Contributors
- [Just-Passersby](https://github.com/Just-Passersby): Database + API + Docker deploy + Project planning
- [Lcd0327](https://github.com/Lcd0327): Frontend development + API integration

# Additional comment
- Markdown notes are stored as plain text in the database.
- Image upload is not implemented; only Markdown files are supported, to reduce complexity.

# LICENSE
leaflink-online is licensed under the [Apache 2.0 License](LICENSE)
