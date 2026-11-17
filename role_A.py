import csv
import math
import os
import tkinter as tk
from collections import defaultdict
from datetime import date, datetime
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'expenses.csv')
FIELDS = ['Date', 'Amount', 'Category', 'Notes']
CATEGORIES = ['餐飲', '交通', '娛樂', '購物', '其他']
BG, WHITE, GREEN, DARK, MUTED = '#F3F6F4', '#FFFFFF', '#17805C', '#1C3029', '#64766D'

def initialize_file():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerow(FIELDS)


def read_records():
    with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def write_records(records):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title('MoneyTrack｜支出記帳系統')
        self.root.geometry('1100x760')
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)
        self.edit_index = None
        self.selected_category = tk.StringVar(value=CATEGORIES[0])
        self.status = tk.StringVar(value='準備就緒｜所有紀錄會自動儲存至 expenses.csv')
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.amount_var = tk.StringVar()
        self.notes_var = tk.StringVar()
        self.total_var = tk.StringVar(value='$0')
        self.today_var = tk.StringVar(value='$0')
        self.count_var = tk.StringVar(value='0')
        self.build_ui()
        self.refresh()

    def label(self, parent, text, size=11, color=DARK, bold=False, **kw):
        return tk.Label(parent, text=text, bg=parent.cget('bg'), fg=color,
                        font=('Microsoft JhengHei UI', size, 'bold' if bold else 'normal'), **kw)

    def card(self, parent, **kw):
        return tk.Frame(parent, bg=WHITE, highlightbackground='#E4EBE7', highlightthickness=1, **kw)

    def button(self, parent, text, command, color=GREEN, fg='white'):
        return tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                         activebackground=color, activeforeground=fg,
                         relief='flat', bd=0, cursor='hand2', padx=15, pady=11,
                         font=('Microsoft JhengHei UI', 10, 'bold'))

    def build_ui(self):
        outer = tk.Frame(self.root, bg=BG, padx=24, pady=20)
        outer.pack(fill='both', expand=True)
        self.label(outer, 'MoneyTrack', 23, DARK, True).pack(anchor='w')
        self.label(outer, '簡單記錄每一天的生活支出', 10, MUTED).pack(anchor='w', pady=(0, 15))

        stats = tk.Frame(outer, bg=BG)
        stats.pack(fill='x', pady=(0, 16))
        for i, (heading, var) in enumerate([('全部支出', self.total_var), ('今日支出', self.today_var), ('紀錄筆數', self.count_var)]):
            stats.grid_columnconfigure(i, weight=1, uniform='stat')
            box = self.card(stats, padx=17, pady=14)
            box.grid(row=0, column=i, sticky='ew', padx=(0 if i == 0 else 6, 0))
            self.label(box, heading, 10, MUTED).pack(anchor='w')
            self.label(box, '', 18, GREEN, True, textvariable=var).pack(anchor='w', pady=(5, 0))

        content = tk.Frame(outer, bg=BG)
        content.pack(fill='both', expand=True)
        content.grid_columnconfigure(0, weight=2)
        content.grid_columnconfigure(1, weight=3)
        content.grid_rowconfigure(0, weight=1)

        left = self.card(content, padx=19, pady=17)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        right = self.card(content, padx=16, pady=17)
        right.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        self.label(left, '新增 / 修改支出', 15, DARK, True).pack(anchor='w', pady=(0, 10))

        self.label(left, '日期（YYYY-MM-DD）', 10, MUTED).pack(anchor='w')
        self.date_entry = ttk.Entry(left, textvariable=self.date_var, font=('Microsoft JhengHei UI', 12))
        self.date_entry.pack(fill='x', ipady=6, pady=(4, 8))
        self.label(left, '金額（元）', 10, MUTED).pack(anchor='w')
        ttk.Entry(left, textvariable=self.amount_var, font=('Microsoft JhengHei UI', 12)).pack(fill='x', ipady=6, pady=(4, 8))
        self.label(left, '支出類別', 10, MUTED).pack(anchor='w')
        self.category_combo = ttk.Combobox(left, textvariable=self.selected_category, values=CATEGORIES, state='readonly', font=('Microsoft JhengHei UI', 11))

        self.category_combo.pack(fill='x', ipady=5, pady=(4, 8))
        self.label(left, '備註（選填）', 10, MUTED).pack(anchor='w')
        ttk.Entry(left, textvariable=self.notes_var, font=('Microsoft JhengHei UI', 12)).pack(fill='x', ipady=6, pady=(4, 10))

        self.button(left, '＋ 新增支出', self.add).pack(fill='x', pady=(0, 9))
        edit_buttons = tk.Frame(left, bg=WHITE)
        edit_buttons.pack(fill='x')
        for i in range(2):
            edit_buttons.grid_columnconfigure(i, weight=1)
        self.button(edit_buttons, '修改選取', self.start_edit, '#E8F2ED', GREEN).grid(row=0, column=0, sticky='ew', padx=(0, 4))
        self.button(edit_buttons, '儲存修改', self.save_edit, '#E8F2ED', GREEN).grid(row=0, column=1, sticky='ew', padx=(4, 0))
        action_buttons = tk.Frame(left, bg=WHITE)
        action_buttons.pack(fill='x', pady=(8, 0))
        action_buttons.grid_columnconfigure(0, weight=1)
        action_buttons.grid_columnconfigure(1, weight=1)
        self.button(action_buttons, '取消修改', self.cancel_edit, '#F0F3F1', DARK).grid(row=0, column=0, sticky='ew', padx=(0, 4))
        self.button(action_buttons, '刪除選取紀錄', self.delete, '#FCEBEA', '#B33A36').grid(row=0, column=1, sticky='ew', padx=(4, 0))
        self.label(left, '日期會保留，方便連續記錄同一天的支出。', 9, MUTED).pack(anchor='w', pady=(9, 0))

        self.label(right, '支出紀錄', 15, DARK, True).pack(anchor='w', pady=(0, 10))
        table_wrap = tk.Frame(right, bg=WHITE)
        table_wrap.pack(fill='both', expand=True)
        style = ttk.Style()
        style.configure('Expense.Treeview', font=('Microsoft JhengHei UI', 10), rowheight=30,
                        background=WHITE, fieldbackground=WHITE, foreground=DARK)
        style.configure('Expense.Treeview.Heading', font=('Microsoft JhengHei UI', 10, 'bold'))
        style.map('Expense.Treeview', background=[('selected', '#D7EBDF')], foreground=[('selected', DARK)])
        cols = ('Date', 'Amount', 'Category', 'Notes')
        self.tree = ttk.Treeview(table_wrap, columns=cols, show='headings', style='Expense.Treeview', selectmode='browse')
        for col, title, width in [('Date', '日期', 115), ('Amount', '金額', 95), ('Category', '類別', 75), ('Notes', '備註', 130)]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, minwidth=60, stretch=True)
        scroll = ttk.Scrollbar(table_wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

        self.label(right, '每日支出統計', 12, DARK, True).pack(anchor='w', pady=(15, 6))
        daily_wrap = tk.Frame(right, bg=WHITE)
        daily_wrap.pack(fill='x')
        self.daily_list = tk.Listbox(daily_wrap, height=5, relief='flat', bg='#F7FAF8', fg=DARK,
                                     font=('Microsoft JhengHei UI', 10), selectbackground='#D7EBDF',
                                     selectforeground=DARK, activestyle='none')
        daily_scroll = ttk.Scrollbar(daily_wrap, orient='vertical', command=self.daily_list.yview)
        self.daily_list.configure(yscrollcommand=daily_scroll.set)
        self.daily_list.pack(side='left', fill='x', expand=True)
        daily_scroll.pack(side='right', fill='y')

        self.status_label = self.label(outer, '', 10, GREEN, textvariable=self.status, anchor='w')
        self.status_label.pack(fill='x', pady=(12, 0))

    def notify(self, message, error=False):
        self.status.set(('✗ ' if error else '✓ ') + message)
        self.status_label.config(fg='#B33A36' if error else GREEN)

    def get_data(self):
        raw_date = self.date_var.get().strip()
        try:
            d = datetime.strptime(raw_date, '%Y-%m-%d')
            if d.strftime('%Y-%m-%d') != raw_date:
                raise ValueError
        except ValueError:
            self.notify('日期格式錯誤，請使用 YYYY-MM-DD', True)
            return None
        try:
            amount = float(self.amount_var.get().strip())
            if not math.isfinite(amount) or amount <= 0:
                raise ValueError
        except ValueError:
            self.notify('金額必須是大於 0 的有效數字', True)
            return None
        category = self.selected_category.get()
        if category not in CATEGORIES:
            self.notify('請選擇支出類別', True)
            return None
        return {'Date': raw_date, 'Amount': str(amount), 'Category': category,
                'Notes': self.notes_var.get().strip()}

    def clear_fields(self):
        self.amount_var.set('')
        self.notes_var.set('')

    def add(self):
        if self.edit_index is not None:
            self.notify('正在修改紀錄，請先儲存或取消修改', True)
            return
        data = self.get_data()
        if data is None:
            return
        with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerow([data[k] for k in FIELDS])
        self.clear_fields()
        self.refresh()
        self.notify('新增支出成功')

    def selected_index(self):
        selected = self.tree.selection()
        if not selected:
            self.notify('請先點選右側的一筆支出紀錄', True)
            return None
        return int(selected[0])

    def start_edit(self):
        idx = self.selected_index()
        if idx is None:
            return
        records = read_records()
        if idx >= len(records):
            self.notify('該筆紀錄已不存在', True)
            return
        row = records[idx]
        self.edit_index = idx
        self.date_var.set(row['Date'])
        self.amount_var.set(row['Amount'])
        self.selected_category.set(row['Category'])
        self.notes_var.set(row['Notes'])
        self.notify('已載入紀錄，修改後請按「儲存修改」')

    def save_edit(self):
        if self.edit_index is None:
            self.notify('請先點選紀錄並按「修改選取」', True)
            return
        data = self.get_data()
        if data is None:
            return
        records = read_records()
        if self.edit_index >= len(records):
            self.notify('原始紀錄已不存在', True)
            self.edit_index = None
            return
        records[self.edit_index] = data
        write_records(records)
        self.edit_index = None
        self.clear_fields()
        self.refresh()
        self.notify('修改成功')

    def cancel_edit(self):
        self.edit_index = None
        self.clear_fields()
        self.notify('已取消修改')

    def delete(self):
        idx = self.selected_index()
        if idx is None:
            return
        records = read_records()
        if idx >= len(records):
            self.notify('該筆紀錄已不存在', True)
            return
        del records[idx]
        write_records(records)
        self.edit_index = None
        self.refresh()
        self.notify('已刪除選取紀錄（不會跳出確認視窗）')

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.daily_list.delete(0, tk.END)
        records = read_records()
        totals = defaultdict(float)
        grand_total = 0.0
        today_total = 0.0
        today = date.today().isoformat()
        for idx, row in sorted(enumerate(records), key=lambda item: item[1]['Date']):
            try:
                amount = float(row['Amount'])
            except (ValueError, TypeError):
                amount = 0.0
            self.tree.insert('', 'end', iid=str(idx), values=(row['Date'], f'{amount:,.2f}', row['Category'], row['Notes']))
            totals[row['Date']] += amount
            grand_total += amount
            if row['Date'] == today:
                today_total += amount
        for day in sorted(totals, reverse=True):
            self.daily_list.insert(tk.END, f'  {day}     NT$ {totals[day]:,.2f}')
        self.total_var.set(f'NT$ {grand_total:,.2f}')
        self.today_var.set(f'NT$ {today_total:,.2f}')
        self.count_var.set(str(len(records)))

if __name__ == '__main__':
    initialize_file()
    root = tk.Tk()
    ExpenseApp(root)
    print('CSV 儲存位置：', CSV_FILE)
    root.mainloop()