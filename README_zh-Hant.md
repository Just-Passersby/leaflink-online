# leaflink-online

[English](README.md) | 繁體中文

## 專案介紹
114年第二學期網頁資料庫程式設計課程期末專題。

啟發於Obsidian，將Obsidian的功能實作成簡單的網頁版。

## 技術棧
### 前端
框架：SvelteKit\
使用Single-page app，搭配HTML和CSS，運行在Nginx上

### 後端
使用FastAPI

### 資料庫
使用PostgreSQL

### 其他
提供Dockerfile和Docker Compose用於快速建立Demo環境。

## 開發環境
### 前端
前端使用[fnm](https://github.com/Schniz/fnm)管理Node.js (SvelteKit依賴Node.js)\
套件管理工具使用`pnpm`\
進入前端開發需要進入`frontend`目錄
開發時使用以下指令：
| 指令 | 說明 |
| :-: | :- |
| `pnpm dev --open`| 運行dev Server監聽開發變化，`Ctrl+C`關閉 |
> 備註： `--open`會自動打開分頁，如果不希望自動打開分頁請把該參數刪除

### 後端
FastAPI (待補充)

### 專案目錄架構
```
leaflink-online
├── frontend/
├── backend/   #待建立
└── README.md
```

## MVP
### 預定目標
- 使用者功能
  - [ ] 註冊功能
  - [ ] 登入 + JWT
- [ ] Vault隱私權設定
- [ ] Markdown筆記 CRUD 與瀏覽
- [ ] Markdown筆記 / Vault上傳
- [ ] `[[雙向連結]]`解析與 Backlinks 顯示
- [ ] 標籤系統與全文搜尋（PostgreSQL tsvector）

### 額外目標
- [ ] 個人線上編輯Markdown筆記和Vault
- [ ] 知識網路(D3.js)

## 資料庫設計
ER圖待補

## 分工
- [Just-Passersby](https://github.com/Just-Passersby): Database + API + Docker部署 + 專題規劃
- [Lcd0327](https://github.com/Lcd0327): 前端開發 + API整合

## 額外說明
- Markdown純文字存在DB內
- 先不做圖片上傳，降低複雜度

## 許可證
leaflink-online使用[Apache 2.0許可證](LICENSE)
