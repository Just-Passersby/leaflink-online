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
前端使用[fnm](https://github.com/Schniz/fnm)管理Node.js (SvelteKit依賴Node.js)\
套件管理工具使用`pnpm`

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

# 額外說明
- Markdown純文字存在DB內
- 先不做圖片上傳，降低複雜度
- Docker Compose等到前端開發完成再做
