# leaflink-online

[English](README.md) | 繁體中文

## 專案介紹
114年第二學期網頁資料庫程式設計課程期末專題。

啟發於 Obsidian，將 Obsidian 的功能實作成簡單的網頁版。

## 技術棧
### 前端
框架：SvelteKit\
使用 Single-page app，搭配 HTML 和 CSS，運行在 Nginx 上

### 後端
使用 FastAPI，透過 Docker 運行

### 資料庫
使用 PostgreSQL

### 其他
提供 Dockerfile 和 Docker Compose 用於快速建立 Demo 環境。

## 開發環境
### 前端
前端使用 [fnm](https://github.com/Schniz/fnm) 管理 Node.js (SvelteKit 依賴 Node.js)\
套件管理工具使用 `pnpm` \
進入前端開發需要進入 `frontend` 目錄
開發時使用以下指令：
|       指令        | 說明                                     |
| :---------------: | :--------------------------------------- |
| `pnpm dev --open` | 運行 dev Server 監聽開發變化，`Ctrl+C` 關閉 |
> 備註： `--open` 會自動打開分頁，如果不希望自動打開分頁請把該參數刪除

### 後端
|   環境   | 說明                                                      |
| :------: | :-------------------------------------------------------- |
|  Python  | 3.12+                                                     |
| 依賴管理 | Astral uv                                                 |
| 開發運行 | `uvicorn main:app --reload`                               |
| 生產運行 | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app` |

### 專案目錄架構
```
leaflink-online
├── frontend/
├── backend/   #待建立
├── db/
└── README.md
```

## MVP
### 預定目標
- 使用者功能
  - [ ] 註冊功能
  - [ ] 登入 + JWT
- [ ] Vault 隱私權設定
- [ ] Markdown 筆記 CRUD 與瀏覽
- [ ] Markdown 筆記 / Vault 上傳
- [ ] `[[雙向連結]]`解析與 Backlinks 顯示
- [ ] 標籤系統與全文搜尋（PostgreSQL tsvector）

### 額外目標
- [ ] 個人線上編輯 Markdown 筆記和 Vault
- [ ] 知識網路(D3.js)

## 資料庫設計
![](./docs/webFP.svg)

## 分工
- [Just-Passersby](https://github.com/Just-Passersby): Database + API + Docker 部署 + 專題規劃
- [Lcd0327](https://github.com/Lcd0327): 前端開發 + API整合

## 額外說明
- Markdown 純文字存在DB內
- 先不做圖片上傳，純 markdown 檔，降低複雜度

## 許可證
leaflink-online 使用 [Apache 2.0 許可證](LICENSE)
