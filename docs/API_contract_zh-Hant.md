# leaflink-online API Contract

> 版本：v1.1 | 狀態：已確認，可開始開發

**v1.1 變更：** 新增 `POST /notes/upload`（單一 .md 檔案上傳）、新增 `BAD_REQUEST` 錯誤碼。

---

## 目錄

1. [全域設定](#1-全域設定)
2. [Error Response 格式](#2-error-response-格式)
3. [Auth 端點](#3-auth-端點)
4. [Vault 端點](#4-vault-端點)
5. [Note 端點](#5-note-端點)
6. [Tag 端點](#6-tag-端點)
7. [Search 端點](#7-search-端點)
8. [分頁格式](#8-分頁格式)
9. [雙向連結解析流程](#9-雙向連結解析流程)

---

## 1. 全域設定

### 認證方式

| 項目 | 設定 |
|---|---|
| 機制 | JWT 存放於 HttpOnly Cookie |
| Cookie 名稱 | `access_token` |
| Cookie 屬性 | `HttpOnly; SameSite=Lax; Secure`（prod），`HttpOnly; SameSite=Lax`（dev） |
| Token 有效期 | 7 天 |

### CORS 設定（FastAPI）

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # dev；prod 改為實際 domain
    allow_credentials=True,                   # 必須 True，否則 cookie 送不出去
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 前端 fetch 設定（SvelteKit）

所有 API 呼叫都必須帶 `credentials: 'include'`，否則 cookie 不會隨請求送出：

```javascript
fetch('/api/...', {
  credentials: 'include',
  // ...
})
```

---

## 2. Error Response 格式

### 統一回傳結構

```json
{
  "code": "VAULT_NOT_FOUND",
  "message": "找不到指定的 Vault",
  "detail": null
}
```

| 欄位 | 型別 | 說明 |
|---|---|---|
| `code` | string | 前端程式判斷用的 enum，見下表 |
| `message` | string | 人讀說明，可直接顯示給使用者 |
| `detail` | any \| null | 額外資訊，validation error 時列出錯誤欄位；其他情況為 null |

### Error Code 一覽

| code | HTTP | 場景 |
|---|---|---|
| `BAD_REQUEST` | 400 | 業務邏輯錯誤（例如上傳非 .md 檔案、檔案非 UTF-8 編碼） |
| `UNAUTHORIZED` | 401 | 未登入或 token 失效 |
| `FORBIDDEN` | 403 | 無權限（不是自己的 vault/note） |
| `NOT_FOUND` | 404 | 資源不存在 |
| `CONFLICT` | 409 | 重複資源（username 或 email 已存在） |
| `VALIDATION_ERROR` | 422 | 欄位格式錯，`detail` 為 FastAPI validation errors array |

### FastAPI 實作

```python
class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, detail=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "請求格式錯誤",
            "detail": exc.errors()
        }
    )

# 使用方式
raise AppError("VAULT_NOT_FOUND", "找不到指定的 Vault", 404)
```

---

## 3. Auth 端點

### POST /auth/register

**需要認證：** 否

**Request Body：**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response 200：**
```json
{
  "id": 1,
  "username": "just-passersby",
  "email": "user@example.com",
  "created_at": "2026-05-22T09:00:00Z"
}
```

**可能的 Error：**
- `409 CONFLICT`：username 或 email 已存在

---

### POST /auth/login

**需要認證：** 否

**Request Body：**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response 200：**
```json
{
  "id": 1,
  "username": "just-passersby",
  "email": "user@example.com"
}
```

Set-Cookie header 同時設定 `access_token`（後端處理，前端不需要額外操作）

**可能的 Error：**
- `401 UNAUTHORIZED`：帳密錯誤

---

### POST /auth/logout

**需要認證：** 是

**Request Body：** 無

**Response 200：**
```json
{ "message": "登出成功" }
```

後端清除 Cookie（設 Max-Age=0）

---

### GET /auth/me

**需要認證：** 是

**Response 200：**
```json
{
  "id": 1,
  "username": "just-passersby",
  "email": "user@example.com",
  "created_at": "2026-05-22T09:00:00Z"
}
```

前端用來確認目前登入狀態，頁面初始化時呼叫。

---

## 4. Vault 端點

### GET /vaults/mine

**需要認證：** 是  
**說明：** 取得自己的所有 vault

**Response 200：**
```json
{
  "items": [
    {
      "id": 1,
      "name": "My Notes",
      "public": true,
      "created_at": "2026-05-22T09:00:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

---

### GET /vaults/explore

**需要認證：** 否  
**說明：** 瀏覽所有公開 vault  
**Query params：** `?page=1&size=20`

**Response 200：** 同上格式，items 內多一個 `owner_username` 欄位

```json
{
  "items": [
    {
      "id": 2,
      "name": "Linux Notes",
      "public": true,
      "owner_username": "just-passersby",
      "created_at": "2026-05-22T09:00:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "size": 20,
  "pages": 3
}
```

---

### GET /vaults/{vault_id}

**需要認證：** public vault 不需要；private vault 需要且必須是 owner  
**Response 200：**
```json
{
  "id": 1,
  "name": "My Notes",
  "public": true,
  "owner_username": "just-passersby",
  "created_at": "2026-05-22T09:00:00Z"
}
```

**可能的 Error：**
- `404 NOT_FOUND`
- `403 FORBIDDEN`：private vault 且非 owner

---

### POST /vaults

**需要認證：** 是

**Request Body：**
```json
{
  "name": "string",
  "public": true
}
```

**Response 201：** 回傳新建的 vault（同 GET /vaults/{id} 格式）

---

### PATCH /vaults/{vault_id}

**需要認證：** 是，且必須是 owner

**Request Body：**（所有欄位可選）
```json
{
  "name": "string",
  "public": true
}
```

**Response 200：** 回傳更新後的 vault

---

### DELETE /vaults/{vault_id}

**需要認證：** 是，且必須是 owner

**Response 204：** No Content  
**注意：** 刪除 vault 會 cascade 刪除旗下所有 notes 和 links

---

## 5. Note 端點

### GET /vaults/{vault_id}/notes

**需要認證：** public vault 不需要；private vault 需要且必須是 owner  
**Query params：** `?page=1&size=20`  
**說明：** list view 用，不含 content，減少傳輸量

**Response 200：**
```json
{
  "items": [
    {
      "id": 1,
      "title": "My Note",
      "vault_id": 1,
      "created_at": "2026-05-22T09:00:00Z",
      "updated_at": "2026-05-22T09:00:00Z",
      "tags": [{ "id": 1, "name": "linux" }]
    }
  ],
  "total": 30,
  "page": 1,
  "size": 20,
  "pages": 2
}
```

---

### GET /notes/{note_id}

**需要認證：** 視所屬 vault 的 public 狀態  
**說明：** 含 content、backlinks、tags（全 inline）

**Response 200：**
```json
{
  "id": 1,
  "title": "My Note",
  "content": "# Hello\n這是一篇筆記，連結到 [[Other Note]]",
  "vault_id": 1,
  "created_at": "2026-05-22T09:00:00Z",
  "updated_at": "2026-05-22T09:00:00Z",
  "tags": [
    { "id": 1, "name": "linux" }
  ],
  "backlinks": [
    { "id": 2, "title": "Other Note" }
  ]
}
```

---

### POST /notes

**需要認證：** 是

**Request Body：**
```json
{
  "vault_id": 1,
  "title": "string",
  "content": "string",
  "tags": ["linux", "btrfs"]
}
```

**說明：**
- `tags` 帶 name array，後端自動 upsert（`ON CONFLICT DO NOTHING`）再寫 `note_tags`
- 後端解析 content 內的 `[[title]]`，查 notes 找 id，寫入 `links` table
- 找不到對應 title 的連結暫時忽略（不報錯）

**Response 201：** 回傳新建的 note（同 GET /notes/{id} 格式）

---

### PATCH /notes/{note_id}

**需要認證：** 是，且必須是所屬 vault 的 owner

**Request Body：**（所有欄位可選）
```json
{
  "title": "string",
  "content": "string",
  "tags": ["linux"]
}
```

**說明：**
- 更新 content 時，後端重新解析 `[[title]]` 並完整替換 `links` table 對應資料
- 更新 tags 時，完整替換 `note_tags`（先刪舊的再寫新的）

**Response 200：** 回傳更新後的 note（同 GET /notes/{id} 格式）

---

### DELETE /notes/{note_id}

**需要認證：** 是，且必須是所屬 vault 的 owner

**Response 204：** No Content  
**注意：** 刪除 note 時需同步刪除 `links` 中所有 `src_note` 或 `dest_note` 為此 note 的資料

---

### POST /notes/upload

**需要認證：** 是，且必須是目標 vault 的 owner  
**Content-Type：** `multipart/form-data`  
**說明：** 上傳單一 `.md` 檔案，自動以檔名（去掉 `.md`）作為 title，檔案內容作為 content。

**Form Fields：**

| 欄位 | 型別 | 必填 | 說明 |
|---|---|:---:|---|
| `file` | File | ✅ | 必須為 `.md` 副檔名，UTF-8 編碼 |
| `vault_id` | int | ✅ | 目標 Vault ID |
| `tags` | string | ❌ | 逗號分隔的 tag 名稱，例如 `"linux,btrfs"` |

**Response 201：** 回傳新建的 note（同 `GET /notes/{id}` 格式）

**可能的 Error：**
- `400 BAD_REQUEST`：檔案非 `.md` 副檔名，或內容無法以 UTF-8 解碼
- `403 FORBIDDEN`：非 vault owner
- `404 NOT_FOUND`：vault 不存在

**後端行為：**
1. 驗證副檔名為 `.md`
2. 讀取檔案內容並以 UTF-8 解碼
3. 以 `filename`（去掉 `.md` 後綴）作為 `title`
4. 後續流程與 `POST /notes` 相同（tags upsert、`[[wikilink]]` 解析）

---

## 6. Tag 端點

Tag 的 CRUD 透過 Note 端點的 `tags` 欄位處理，不提供獨立的 tag 管理 endpoint。

### GET /tags

**需要認證：** 否  
**說明：** 取得所有 tag（用於搜尋 autocomplete）

**Response 200：**
```json
[
  { "id": 1, "name": "linux" },
  { "id": 2, "name": "btrfs" }
]
```

資料量不大，不分頁。

---

## 7. Search 端點

### GET /search

**需要認證：** 否（只搜尋公開 vault 的 notes；登入後也搜尋自己的 private notes）  
**Query params：** `?q=keyword&page=1&size=20`

**Response 200：**
```json
{
  "items": [
    {
      "id": 1,
      "title": "My Note",
      "vault_id": 1,
      "vault_name": "Linux Notes",
      "owner_username": "just-passersby",
      "updated_at": "2026-05-22T09:00:00Z",
      "tags": [{ "id": 1, "name": "linux" }]
    }
  ],
  "total": 5,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

**後端實作備注：** 使用 PostgreSQL `tsvector`，在 `notes` 表加 generated column：

```sql
ALTER TABLE notes ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (to_tsvector('simple', title || ' ' || content)) STORED;

CREATE INDEX notes_search_idx ON notes USING GIN(search_vector);
```

查詢：`WHERE search_vector @@ plainto_tsquery('simple', :q)`

---

## 8. 分頁格式

### Request

Query params：`?page=1&size=20`

| param | 預設值 | 限制 |
|---|---|---|
| `page` | 1 | >= 1 |
| `size` | 20 | 1–100 |

### Response

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "size": 20,
  "pages": 3
}
```

| 欄位 | 說明 |
|---|---|
| `items` | 當頁資料 |
| `total` | 總筆數 |
| `page` | 當前頁 |
| `size` | 每頁筆數 |
| `pages` | 總頁數（`ceil(total / size)`） |

### 哪些 endpoint 有分頁

| Endpoint | 分頁 |
|---|---|
| `GET /vaults/mine` | ✅ |
| `GET /vaults/explore` | ✅ |
| `GET /vaults/{id}/notes` | ✅ |
| `GET /search` | ✅ |
| `GET /notes/{id}`（含 backlinks、tags） | ❌ inline |
| `GET /tags` | ❌ |

---

## 9. 雙向連結解析流程

**責任歸屬：後端**

### 建立/更新 note 時

```
1. 接收 content（raw markdown）
2. Regex 提取所有 [[title]] 語法
3. 對每個 title 查詢同 vault 內是否有對應 note
4. 找到 → 寫入 links table (src_note=當前 id, dest_note=對方 id)
5. 找不到 → 暫時忽略，不報錯
6. PATCH 時：先刪除此 note 所有舊 src_note 記錄，再重新寫入
```

### GET /notes/{id} 回傳 backlinks 時

```sql
SELECT n.id, n.title
FROM notes n
JOIN links l ON l.src_note = n.id
WHERE l.dest_note = :note_id
```

### 前端渲染

前端拿到 raw markdown 後，自行將 `[[title]]` 渲染成可點擊連結（導向對應 note 頁面），不需要後端額外處理。