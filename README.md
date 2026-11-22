Team Members
學號	姓名	負責功能
1132917	蘇佩璇	Input module（Member A）
1132914	高彥怜	Visualization module（Member B）
		
Features
Role A — Expense Input Module
•	新增支出紀錄，包含日期、金額、類別及備註
•	支援修改與刪除支出紀錄
•	自動儲存支出資料至 expenses.csv
•	顯示全部支出、今日支出及紀錄筆數
•	顯示每日支出統計
Role B — Expense Visualization Module
•	讀取 expenses.csv 中的支出紀錄
•	依照消費類別統計支出金額
•	使用圓餅圖顯示各類別的支出比例
•	提供日期篩選功能
•	支援重新整理資料及匯出圓餅圖圖片

Development Environment
•	Programming Language：Python 3
•	GUI Framework：Tkinter
•	Data Storage：CSV
•	Version Control：Git
•	Repository Hosting：GitHub

Installation
點進網址 : https://github.com/sunniening-lang/expense-tracker
下載:
<img width="865" height="507" alt="image" src="https://github.com/user-attachments/assets/7d3f0d22-11fd-4cde-af63-788f099e75fc" />
下載完後解壓縮即可

本專案使用 Python 標準函式庫，不需要另外安裝第三方 Python 套件
請確認電腦已安裝 Python，並且 Python 環境支援 Tkinter

How to Run
請先確認電腦已安裝 Python 3。
下載並解壓縮專案後，在專案資料夾開啟終端機，輸入：
python main.py
執行後會同時開啟兩個視窗：
•	Role A（Input module）：新增、修改、刪除支出紀錄
•	Role B（Visualization module）：讀取支出資料，顯示各類別的圓餅圖
也可以分別執行：
python role_A.py
python role_B.py
兩個程式共用 expenses.csv，Role A 更新資料後，Role B 會自動更新圓餅圖

Usage Instructions
1.	開啟程式
2.	輸入日期、金額、消費類別及備註
(日期預設為當日日期、備註可以省略)
3.	點擊「新增支出」，將資料儲存至 CSV 檔案
4.	開啟支出視覺化模組 (預設開啟在右邊可以自行關掉)
5.	可查看不同類別的支出金額與圓餅圖
6.	可依日期篩選資料，查看特定日期的支出分布圓餅圖
**可以點選已經新增的支出隨後點擊修改選取後修改資料最後點擊儲存修
  改，修改資料
**可以點選已經新增的支出隨後點擊刪除選取紀錄刪除支出
(可參考最後的Demo Video)

Sample Pie Chart
以下為系統產生的支出類別圓餅圖：
![Uploading image.png…]()

Demonstration Video（展示影片）
Demo Video：
https://youtu.be/5LnY6eijXVY

