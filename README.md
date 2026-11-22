
# MoneyTrack — Expense Tracking System

## Team Members

| 學號 | 姓名 | 負責功能 |
|---|---|---|
| 1132917 | 蘇佩璇 | Input module（Member A） |
| 1132914 | 高彥怜 | Visualization module（Member B） |

## Features

### Role A — Expense Input Module

- 新增支出紀錄，包含日期、金額、類別及備註
- 支援修改與刪除支出紀錄
- 自動儲存支出資料至 `expenses.csv`
- 顯示全部支出、今日支出及紀錄筆數
- 顯示每日支出統計

### Role B — Expense Visualization Module

- 讀取 `expenses.csv` 中的支出紀錄
- 依照消費類別統計支出金額
- 使用圓餅圖顯示各類別的支出比例
- 提供日期篩選功能
- 支援重新整理資料及匯出圓餅圖圖片

## Development Environment

- **Programming Language：** Python 3
- **GUI Framework：** Tkinter
- **Data Storage：** CSV
- **Version Control：** Git
- **Repository Hosting：** GitHub

## Installation

### Step 1：下載專案

前往 GitHub Repository：

https://github.com/sunniening-lang/expense-tracker

點選 **Code → Download ZIP** 下載專案。

<img width="865" height="507" alt="GitHub Download ZIP 操作畫面" src="https://github.com/user-attachments/assets/7d3f0d22-11fd-4cde-af63-788f099e75fc" />

### Step 2：解壓縮

下載完成後，將 ZIP 檔案解壓縮至指定資料夾。

### Step 3：確認 Python 環境

本專案使用 Python 標準函式庫，不需要另外安裝第三方 Python 套件。

**請確認電腦已安裝 Python 3，並且 Python 環境支援 Tkinter。**

## How to Run

### 方法一：使用 main.py 同時啟動

下載並解壓縮專案後，在專案資料夾開啟終端機，輸入：

```bash
python main.py
```

執行後會同時開啟兩個視窗：

- **Role A（Input module）：** 新增、修改、刪除支出紀錄
- **Role B（Visualization module）：** 讀取支出資料，顯示各類別的圓餅圖

### 方法二：分別啟動兩個模組

開啟 Role A：

```bash
python role_A.py
```

開啟 Role B：

```bash
python role_B.py
```

**資料同步說明：**

兩個程式共用 `expenses.csv`，Role A 更新資料後，Role B 會自動偵測資料變動並更新圓餅圖。

## Usage Instructions

### 1. 新增支出紀錄

1. 開啟程式。
2. 輸入日期、金額、消費類別及備註。
   - 日期預設為當日日期。
   - 備註可以省略。
3. 點擊「新增支出」，將資料儲存至 CSV 檔案。

### 2. 查看支出圓餅圖

1. 開啟支出視覺化模組（使用 `main.py` 時會同時啟動）。
2. 查看不同類別的支出金額與圓餅圖。
3. 可依日期篩選資料，查看特定日期的支出分布圓餅圖。

### 3. 修改支出紀錄

1. 在 Role A 的支出紀錄中選取要修改的資料。
2. 點擊「修改選取」。
3. 修改日期、金額、類別或備註。
4. 點擊「儲存修改」完成更新。

### 4. 刪除支出紀錄

1. 在 Role A 的支出紀錄中選取要刪除的資料。
2. 點擊「刪除選取紀錄」。
3. 系統會刪除該筆支出紀錄。

**詳細操作過程可參考下方 Demo Video。**

## Sample Pie Chart

以下為系統產生的支出類別圓餅圖：

<img width="817" height="602" alt="MoneyTrack 支出類別圓餅圖" src="https://github.com/user-attachments/assets/62c3d43d-936b-4e30-b435-8a1540e7c29c" />

## Demonstration Video

[觀看 MoneyTrack Demo Video](https://youtu.be/5LnY6eijXVY)


Demonstration Video
Demo Video ： https://youtu.be/5LnY6eijXVY

