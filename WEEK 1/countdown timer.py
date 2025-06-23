import tkinter as tk
from tkinter import messagebox
import time
import threading

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("380x320")
        self.running = False
        self.original_time = 0
        
        # Time input
        tk.Label(root, text="Enter time (MM:SS or seconds):").pack(pady=5)
        self.time_var = tk.StringVar()
        self.time_entry = tk.Entry(root, textvariable=self.time_var, font=('Arial', 14))
        self.time_entry.pack(pady=5)
        
        # Quick add buttons
        quick_add_frame = tk.Frame(root)
        quick_add_frame.pack(pady=5)
        
        tk.Button(quick_add_frame, text="+30s", command=lambda: self.add_time(30)).pack(side=tk.LEFT, padx=5)
        tk.Button(quick_add_frame, text="+1m", command=lambda: self.add_time(60)).pack(side=tk.LEFT, padx=5)
        tk.Button(quick_add_frame, text="+5m", command=lambda: self.add_time(300)).pack(side=tk.LEFT, padx=5)
        tk.Button(quick_add_frame, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("00:00")
        self.display = tk.Label(root, textvariable=self.display_var, font=('Arial', 48))
        self.display.pack(pady=20)
        
        # Control buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start_timer)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_timer, state=tk.DISABLED)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
    def add_time(self, seconds):
        current = self.time_var.get()
        try:
            if ':' in current:
                mins, secs = map(int, current.split(':'))
                total = mins * 60 + secs + seconds
            else:
                total = int(current) + seconds if current else seconds
                
            mins, secs = divmod(total, 60)
            self.time_var.set(f"{mins}:{secs:02d}")
        except ValueError:
            self.time_var.set(str(seconds))
    
    def clear_all(self):
        self.time_var.set("")
        self.display_var.set("00:00")
        if self.running:
            self.stop_timer()
        self.reset_btn.config(state=tk.DISABLED)
    
    def start_timer(self):
        if self.running:
            return
            
        time_str = self.time_var.get()
        try:
            if ':' in time_str:
                mins, secs = map(int, time_str.split(':'))
                total_seconds = mins * 60 + secs
            else:
                total_seconds = int(time_str)
                
            if total_seconds <= 0:
                messagebox.showerror("Error", "Please enter a positive time value")
                return
                
            self.original_time = total_seconds
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.DISABLED)
            
            threading.Thread(target=self.run_timer, args=(total_seconds,), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use MM:SS or seconds")
    
    def run_timer(self, total_seconds):
        end_time = time.time() + total_seconds
        
        while self.running and time.time() < end_time:
            remaining = max(0, end_time - time.time())
            mins, secs = divmod(int(remaining), 60)
            self.display_var.set(f"{mins:02d}:{secs:02d}")
            time.sleep(0.1)
            
        if self.running:  # Only notify if not stopped manually
            self.running = False
            self.display_var.set("00:00")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Timer", "Time's up!")
            self.root.bell()
    
    def stop_timer(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.NORMAL)
    
    def reset_timer(self):
        mins, secs = divmod(self.original_time, 60)
        self.display_var.set(f"{mins:02d}:{secs:02d}")
        self.time_var.set(f"{mins}:{secs:02d}")
        self.reset_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()