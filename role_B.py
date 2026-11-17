import csv
import math
import os
import tkinter as tk
from collections import defaultdict
from datetime import datetime
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'expenses.csv')
CATEGORIES = ['餐飲', '交通', '娛樂', '購物', '其他']
COLORS = ['#17805C', '#5A9ED6', '#F2B65D', '#A78BD1', '#E78383']
BG, WHITE, GREEN, DARK, MUTED = '#F3F6F4', '#FFFFFF', '#17805C', '#1C3029', '#64766D'


class PieChartApp:
    def __init__(self, root):
        self.root = root
        root.title('MoneyTrack｜支出類別分析（Role B）')
        root.geometry('1040x740')
        root.minsize(820, 620)
        root.configure(bg=BG)
        self.filter_var = tk.StringVar(value='全部日期')
        self.status_var = tk.StringVar(value='準備就緒｜讀取與 Role A 相同的 expenses.csv')
        self.total_var = tk.StringVar(value='NT$ 0.00')
        self.count_var = tk.StringVar(value='0')
        self.category_var = tk.StringVar(value='0')
        self.summary = []
        self.build_ui()
        self.refresh()
        self._csv_signature = self.csv_signature()
        self.root.after(1000, self.watch_csv)

    def csv_signature(self):
        """以修改時間與檔案大小偵測 Role A 儲存的變更。"""
        try:
            stat = os.stat(CSV_FILE)
            return (stat.st_mtime_ns, stat.st_size)
        except OSError:
            return None

    def watch_csv(self):
        """每秒檢查一次 CSV，變更時自動刷新，不阻塞 Tkinter 視窗。"""
        current = self.csv_signature()
        if current != self._csv_signature:
            self._csv_signature = current
            # 避免新增到其他日期時仍停留在舊日期的篩選結果。
            #self.filter_var.set('全部日期')
            try:
                self.refresh()
                self.notify('偵測到支出資料變更，圓餅圖已自動更新')
            except (OSError, ValueError, csv.Error) as exc:
                self.notify(f'自動更新失敗：{exc}', True)
        self.root.after(1000, self.watch_csv)

    def label(self, parent, text, size=11, color=DARK, bold=False, **kwargs):
        return tk.Label(parent, text=text, bg=parent.cget('bg'), fg=color,
                        font=('Microsoft JhengHei UI', size, 'bold' if bold else 'normal'), **kwargs)

    def card(self, parent, **kwargs):
        return tk.Frame(parent, bg=WHITE, highlightbackground='#E4EBE7', highlightthickness=1, **kwargs)

    def button(self, parent, text, command, bg=GREEN, fg=WHITE):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=bg, activeforeground=fg, relief='flat', bd=0,
                         cursor='hand2', padx=14, pady=9,
                         font=('Microsoft JhengHei UI', 10, 'bold'))

    def build_ui(self):
        outer = tk.Frame(self.root, bg=BG, padx=24, pady=18)
        outer.pack(fill='both', expand=True)
        self.label(outer, 'MoneyTrack', 23, DARK, True).pack(anchor='w')
        self.label(outer, '支出類別分析｜圓餅圖', 10, MUTED).pack(anchor='w', pady=(0, 14))

        stats = tk.Frame(outer, bg=BG)
        stats.pack(fill='x', pady=(0, 14))
        for i, (heading, var) in enumerate([
            ('篩選後總支出', self.total_var),
            ('支出紀錄筆數', self.count_var),
            ('有支出的類別', self.category_var)
        ]):
            stats.grid_columnconfigure(i, weight=1, uniform='stat')
            box = self.card(stats, padx=16, pady=12)
            box.grid(row=0, column=i, sticky='ew', padx=(0 if i == 0 else 6, 0))
            self.label(box, heading, 10, MUTED).pack(anchor='w')
            self.label(box, '', 18, GREEN, True, textvariable=var).pack(anchor='w', pady=(4, 0))

        controls = self.card(outer, padx=14, pady=12)
        controls.pack(fill='x', pady=(0, 14))
        self.label(controls, '日期篩選', 10, MUTED).pack(side='left', padx=(0, 10))
        self.filter_combo = ttk.Combobox(controls, textvariable=self.filter_var,
                                         state='readonly', width=20,
                                         font=('Microsoft JhengHei UI', 10))
        self.filter_combo.pack(side='left', padx=(0, 12))
        self.filter_combo.bind('<<ComboboxSelected>>', lambda event: self.refresh())
        self.button(controls, '重新讀取 CSV', self.refresh).pack(side='left', padx=(0, 8))
        self.button(controls, '儲存圓餅圖', self.save_chart, '#E8F2ED', GREEN).pack(side='left')

        content = tk.Frame(outer, bg=BG)
        content.pack(fill='both', expand=True)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        chart_card = self.card(content, padx=16, pady=14)
        chart_card.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        self.label(chart_card, '各類別支出比例', 15, DARK, True).pack(anchor='w', pady=(0, 8))
        self.canvas = tk.Canvas(chart_card, bg=WHITE, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda event: self.draw_chart())

        detail_card = self.card(content, padx=16, pady=14)
        detail_card.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        self.label(detail_card, '類別明細', 15, DARK, True).pack(anchor='w', pady=(0, 10))
        self.details = tk.Frame(detail_card, bg=WHITE)
        self.details.pack(fill='both', expand=True)
        self.label(detail_card, '資料來源：expenses.csv（僅讀取）', 9, MUTED).pack(anchor='w', pady=(10, 0))

        self.status_label = self.label(outer, '', 10, GREEN, textvariable=self.status_var, anchor='w')
        self.status_label.pack(fill='x', pady=(10, 0))

    def notify(self, message, error=False):
        self.status_var.set(('✗ ' if error else '✓ ') + message)
        self.status_label.config(fg='#B33A36' if error else GREEN)

    def read_records(self):
        if not os.path.exists(CSV_FILE):
            self.notify('找不到 expenses.csv，請先執行 role_A.py 新增支出', True)
            return []
        try:
            with open(CSV_FILE, newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                if not reader.fieldnames or not all(key in reader.fieldnames for key in ['Date', 'Amount', 'Category', 'Notes']):
                    self.notify('CSV 欄位必須包含 Date, Amount, Category, Notes', True)
                    return []
                return list(reader)
        except (OSError, UnicodeError, csv.Error) as exc:
            self.notify(f'讀取 CSV 失敗：{exc}', True)
            return []

    def refresh(self):
        records = self.read_records()
        dates = sorted({row.get('Date', '') for row in records if row.get('Date')}, reverse=True)
        options = ['全部日期'] + dates
        previous = self.filter_var.get()
        self.filter_combo['values'] = options
        self.filter_var.set(previous if previous in options else '全部日期')
        selected = self.filter_var.get()
        totals = defaultdict(float)
        count = 0
        invalid = 0
        for row in records:
            if selected != '全部日期' and row.get('Date') != selected:
                continue
            try:
                amount = float(row.get('Amount', ''))
                if not math.isfinite(amount) or amount <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                invalid += 1
                continue
            category = row.get('Category', '').strip() or '其他'
            totals[category] += amount
            count += 1

        order = CATEGORIES + sorted(set(totals) - set(CATEGORIES))
        self.summary = [(name, totals[name]) for name in order if totals[name] > 0]
        grand_total = sum(amount for _, amount in self.summary)
        self.total_var.set(f'NT$ {grand_total:,.2f}')
        self.count_var.set(str(count))
        self.category_var.set(str(len(self.summary)))
        self.draw_details(grand_total)
        self.draw_chart()
        self.root.after_idle(self.draw_chart)
        if invalid:
            self.notify(f'分析完成，略過 {invalid} 筆金額無效的紀錄', True)
        elif os.path.exists(CSV_FILE):
            self.notify(f'分析完成｜共 {count} 筆有效紀錄')

    def draw_details(self, grand_total):
        for widget in self.details.winfo_children():
            widget.destroy()
        if not self.summary:
            self.label(self.details, '目前沒有可顯示的支出資料', 11, MUTED).pack(anchor='w', pady=15)
            return
        for i, (name, amount) in enumerate(self.summary):
            color = COLORS[CATEGORIES.index(name) % len(COLORS)] if name in CATEGORIES else '#82958A'
            row = tk.Frame(self.details, bg=WHITE)
            row.pack(fill='x', pady=8)
            tk.Label(row, bg=color, width=2, height=1).pack(side='left', padx=(0, 9))
            self.label(row, name, 11, DARK, True).pack(side='left')
            self.label(row, f'{amount / grand_total * 100:.1f}%', 10, MUTED).pack(side='right')
            self.label(self.details, f'NT$ {amount:,.2f}', 10, GREEN).pack(anchor='w', padx=27)
            ttk.Separator(self.details, orient='horizontal').pack(fill='x', pady=(7, 0))

    def draw_chart(self):
        self.canvas.delete('all')
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            return
        if not self.summary:
            self.canvas.create_text(width / 2, height / 2, text='尚無支出資料\n請先使用 Role A 新增紀錄',
                                    fill=MUTED, font=('Microsoft JhengHei UI', 13), justify='center')
            return
        total = sum(amount for _, amount in self.summary)
        diameter = max(60, min(width - 50, height - 55, 350))
        cx, cy = width / 2, height / 2
        x0, y0, x1, y1 = cx - diameter / 2, cy - diameter / 2, cx + diameter / 2, cy + diameter / 2
        # Tkinter Canvas 的 create_arc(extent=360) 在部分環境會顯示空白。
        # 只有一種類別時，直接畫完整圓形，避免 100% 圓餅圖消失。
        if len(self.summary) == 1:
            name, _ = self.summary[0]
            color = COLORS[CATEGORIES.index(name) % len(COLORS)] if name in CATEGORIES else '#82958A'
            self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline=WHITE, width=2)
            self.canvas.create_text(cx, cy, text='100%', fill=WHITE,
                                    font=('Microsoft JhengHei UI', 22, 'bold'))
            return
        start = 90
        for name, amount in self.summary:
            extent = amount / total * 360
            color = COLORS[CATEGORIES.index(name) % len(COLORS)] if name in CATEGORIES else '#82958A'
            self.canvas.create_arc(x0, y0, x1, y1, start=start, extent=extent,
                                   fill=color, outline=WHITE, width=2, style='pieslice')
            if extent >= 24:
                mid = math.radians(start + extent / 2)
                radius = diameter * 0.32
                tx = cx + radius * math.cos(mid)
                ty = cy - radius * math.sin(mid)
                self.canvas.create_text(tx, ty, text=f'{extent / 3.6:.1f}%', fill=WHITE,
                                        font=('Microsoft JhengHei UI', 10, 'bold'))
            start += extent

    def save_chart(self):
        if not self.summary:
            self.notify('目前沒有圓餅圖可以儲存', True)
            return
        # 使用 Python 標準函式庫直接建立 PNG，不需要 matplotlib 或 Pillow。
        import struct
        import zlib

        width = height = 640
        cx = cy = 320
        radius = 240
        total = sum(amount for _, amount in self.summary)
        sections = []
        cumulative = 0.0
        for name, amount in self.summary:
            cumulative += amount / total * 360
            hex_color = COLORS[CATEGORIES.index(name) % len(COLORS)] if name in CATEGORIES else '#82958A'
            rgb = tuple(bytes.fromhex(hex_color.lstrip('#')))
            sections.append((cumulative, rgb))

        raw = bytearray()
        for y in range(height):
            raw.append(0)  # PNG filter type 0
            for x in range(width):
                dx, dy = x - cx, y - cy
                if dx * dx + dy * dy > radius * radius:
                    raw.extend((255, 255, 255))
                else:
                    angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360
                    color = sections[-1][1]
                    for boundary, rgb in sections:
                        if angle < boundary:
                            color = rgb
                            break
                    raw.extend(color)

        def chunk(kind, data):
            return (struct.pack('>I', len(data)) + kind + data +
                    struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff))

        png = (b'\x89PNG\r\n\x1a\n' +
               chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) +
               chunk(b'IDAT', zlib.compress(bytes(raw), level=6)) +
               chunk(b'IEND', b''))
        path = os.path.join(BASE_DIR, 'category_pie_chart.png')
        try:
            with open(path, 'wb') as file:
                file.write(png)
            self.notify('已儲存 category_pie_chart.png（可放入 README）')
        except OSError as exc:
            self.notify(f'儲存失敗：{exc}', True)


if __name__ == '__main__':
    root = tk.Tk()
    PieChartApp(root)
    print('CSV 讀取位置：', CSV_FILE)
    root.mainloop()