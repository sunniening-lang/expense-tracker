"""將 main.py、role_A.py、role_B.py 放在同一資料夾，執行 python main.py。"""

import tkinter as tk

import role_A
import role_B


def arrange_windows(root, analysis_window):
    """啟動時將記帳放左邊、分析放右邊。"""
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    height = max(1, root.winfo_screenheight() - 100)
    margin = 8
    gap = 16
    available_width = max(2, screen_width - margin * 2 - gap)
    left_width = available_width // 2
    right_width = available_width - left_width

    # 允許兩個視窗縮至半個螢幕寬度。
    for window in (root, analysis_window):
        window.minsize(1, 1)
    root.geometry(f'{left_width}x{height}+{margin}+{margin}')
    analysis_window.geometry(
        f'{right_width}x{height}+{margin + left_width + gap}+{margin}'
    )


def main():
    role_A.initialize_file()

    root = tk.Tk()
    expense_app = role_A.ExpenseApp(root)

    analysis_window = tk.Toplevel(root)
    analysis_app = role_B.PieChartApp(analysis_window)

    # 記帳視窗是主視窗，關閉它時會結束整個應用程式。
    # 保留分析視窗及其自動更新排程，關閉時先隱藏。
    analysis_window.protocol('WM_DELETE_WINDOW', analysis_window.withdraw)
    menu = tk.Menu(root)
    menu.add_command(label='開啟類別分析', command=analysis_window.deiconify)
    root.configure(menu=menu)

    analysis_menu = tk.Menu(analysis_window)
    analysis_menu.add_command(label='  ', command=root.lift)
    analysis_window.configure(menu=analysis_menu)

    arrange_windows(root, analysis_window)

    print('CSV 儲存位置：', role_A.CSV_FILE)
    root.mainloop()


if __name__ == '__main__':
    main()
