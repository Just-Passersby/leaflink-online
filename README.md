# leaflink-online

[繁體中文](README_zh-Hant.md) | English

115-2 Web and Database course Project, inspired by Obsidian.

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
Developing using command as follows:
|      Command      | Description                                                          |
| :---------------: | :------------------------------------------------------------------- |
| `pnpm dev --open` | Runs the dev Server and watches for changes. Press `Ctrl+C` to stop. |
> Note: Using `--open` will automatically open the app in a new browser tab.\
> If you don't want this behavior, remove the `--open` flag.
