# leaflink-online

[繁體中文](README_zh-Hant.md) | English

114-2 Web and Database course Project, inspired by Obsidian.

A simple web-based implementation of Obsidian's core features.

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
  - [ ] User registration
  - [ ] Login + JWT
- [ ] Vault privacy settings
- [ ] Markdown notes CRUD and browsing
- [ ] Markdown notes and vaults upload
- [ ] `[[Bi-directional links]]` resolve and backlink display
- [ ] Tags system and Full-text search engine (PostgreSQL tsvector)

### Additional targets
- [ ] Personal online Markdown note and vaults editing
- [ ] Knowledge network (D3.js)

## Database design
![](./docs/webFP.svg)
