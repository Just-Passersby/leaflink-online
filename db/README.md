# Database

leaflink-online 使用 PostgreSQL 17，透過 Docker 運行。

## 前置需求

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose

## 設定

在**專案根目錄**複製環境變數範本並填入密碼：

```bash
cp .env.example .env
```

編輯 `.env`，將 `POSTGRES_PASSWORD` 改為自訂密碼：

```
POSTGRES_DB=leaflink
POSTGRES_USER=leaflink
POSTGRES_PASSWORD=your_password_here
```

## 單獨啟動資料庫

從**專案根目錄**執行：

```bash
docker compose up db -d
```

停止：

```bash
docker compose stop db
```

清除資料（重置 DB）：

```bash
docker compose down -v
```

> **注意：** `-v` 會刪除 volume，資料庫內所有資料將清空。

## 連線資訊

| 項目 | 值 |
|---|---|
| Host | `localhost` |
| Port | `5432` |
| Database | `leaflink`（或 `.env` 內的 `POSTGRES_DB`） |
| Username | `leaflink`（或 `.env` 內的 `POSTGRES_USER`） |

Connection string（後端使用）：

```
postgresql://leaflink:<password>@localhost:5432/leaflink
```

用 `psql` 連線：

```bash
docker compose exec db psql -U leaflink -d leaflink
```

## Schema

Schema 定義於 `init.sql`，PostgreSQL 容器**首次啟動**時自動執行。若需重新套用 schema，須先執行 `docker compose down -v` 清除 volume。
