#!/usr/bin/env python3
"""
Simple GUI for Social Media Report Generator
Provides a file picker and generate button instead of command line.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import webbrowser
import threading

class ReportGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Report Generator")
        self.root.geometry("500x400")
        self.root.configure(bg='#FAF9F7')
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.auto_open = tk.BooleanVar(value=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#FAF9F7', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title = tk.Label(main_frame, text="Report Generator", 
                        font=('Segoe UI', 24, 'bold'), bg='#FAF9F7', fg='#1A1A1A')
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(main_frame, text="Convert Word documents to beautiful HTML reports",
                           font=('Segoe UI', 10), bg='#FAF9F7', fg='#6B6B6B')
        subtitle.pack(pady=(0, 30))
        
        # Input file section
        input_frame = tk.LabelFrame(main_frame, text="Input File", 
                                   font=('Segoe UI', 10, 'bold'), bg='#FAF9F7', fg='#1A1A1A',
                                   padx=15, pady=15)
        input_frame.pack(fill='x', pady=(0, 15))
        
        input_entry = tk.Entry(input_frame, textvariable=self.input_file, 
                              font=('Segoe UI', 10), width=40)
        input_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(input_frame, text="Browse...", command=self.browse_input,
                              font=('Segoe UI', 9), bg='#2D2D2D', fg='white',
                              relief='flat', padx=15, pady=5, cursor='hand2')
        browse_btn.pack(side='right')
        
        # Output file section
        output_frame = tk.LabelFrame(main_frame, text="Output File (optional)", 
                                    font=('Segoe UI', 10, 'bold'), bg='#FAF9F7', fg='#1A1A1A',
                                    padx=15, pady=15)
        output_frame.pack(fill='x', pady=(0, 15))
        
        output_entry = tk.Entry(output_frame, textvariable=self.output_file, 
                               font=('Segoe UI', 10), width=40)
        output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        output_btn = tk.Button(output_frame, text="Browse...", command=self.browse_output,
                              font=('Segoe UI', 9), bg='#2D2D2D', fg='white',
                              relief='flat', padx=15, pady=5, cursor='hand2')
        output_btn.pack(side='right')
        
        # Options
        options_frame = tk.Frame(main_frame, bg='#FAF9F7')
        options_frame.pack(fill='x', pady=(0, 20))
        
        auto_open_check = tk.Checkbutton(options_frame, text="Open report in browser after generating",
                                        variable=self.auto_open, bg='#FAF9F7', fg='#1A1A1A',
                                        font=('Segoe UI', 10), activebackground='#FAF9F7')
        auto_open_check.pack(anchor='w')
        
        # Generate button
        self.generate_btn = tk.Button(main_frame, text="Generate Report", 
                                     command=self.generate_report,
                                     font=('Segoe UI', 12, 'bold'), bg='#C4A484', fg='white',
                                     relief='flat', padx=30, pady=12, cursor='hand2')
        self.generate_btn.pack(pady=(10, 15))
        
        # Status label
        self.status_label = tk.Label(main_frame, text="", font=('Segoe UI', 10), 
                                    bg='#FAF9F7', fg='#6B6B6B')
        self.status_label.pack()
        
        # Progress bar (hidden initially)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=300)
    
    def browse_input(self):
        # Start in the Content_Schedule_INPUT folder if it exists
        initial_dir = os.path.join(os.path.dirname(__file__), 'Content_Schedule_INPUT')
        if not os.path.exists(initial_dir):
            initial_dir = os.path.dirname(__file__)
        
        filename = filedialog.askopenfilename(
            title="Select Word Document",
            initialdir=initial_dir,
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-set output filename
            if not self.output_file.get():
                output_dir = os.path.join(os.path.dirname(__file__), 'Content_Schedule_OUTPUT')
                if not os.path.exists(output_dir):
                    output_dir = os.path.dirname(filename)
                base_name = os.path.splitext(os.path.basename(filename))[0]
                self.output_file.set(os.path.join(output_dir, f"{base_name}_report.html"))
    
    def browse_output(self):
        initial_dir = os.path.join(os.path.dirname(__file__), 'Content_Schedule_OUTPUT')
        if not os.path.exists(initial_dir):
            initial_dir = os.path.dirname(__file__)
            
        filename = filedialog.asksaveasfilename(
            title="Save Report As",
            initialdir=initial_dir,
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def generate_report(self):
        input_file = self.input_file.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"File not found: {input_file}")
            return
        
        # Disable button and show progress
        self.generate_btn.config(state='disabled', text="Generating...")
        self.status_label.config(text="Processing document...", fg='#F57C00')
        self.progress.pack(pady=(10, 0))
        self.progress.start()
        self.root.update()
        
        # Run generation in background thread
        thread = threading.Thread(target=self._run_generation)
        thread.start()
    
    def _run_generation(self):
        try:
            input_file = self.input_file.get()
            output_file = self.output_file.get()
            
            # Build command
            script_path = os.path.join(os.path.dirname(__file__), 'generate_report.py')
            cmd = ['python', script_path, input_file]
            if output_file:
                cmd.append(output_file)
            
            # Run the script
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
            
            # Update UI in main thread
            self.root.after(0, lambda: self._on_generation_complete(result, output_file or input_file.replace('.docx', '_report.html')))
            
        except Exception as e:
            self.root.after(0, lambda: self._on_generation_error(str(e)))
    
    def _on_generation_complete(self, result, output_file):
        self.progress.stop()
        self.progress.pack_forget()
        self.generate_btn.config(state='normal', text="Generate Report")
        
        if result.returncode == 0:
            self.status_label.config(text="✓ Report generated successfully!", fg='#2E7D32')
            
            if self.auto_open.get() and os.path.exists(output_file):
                webbrowser.open('file://' + os.path.abspath(output_file))
            
            messagebox.showinfo("Success", f"Report generated!\n\n{output_file}")
        else:
            self.status_label.config(text="✗ Error generating report", fg='#C62828')
            error_msg = result.stderr if result.stderr else result.stdout
            messagebox.showerror("Error", f"Failed to generate report:\n\n{error_msg[:500]}")
    
    def _on_generation_error(self, error):
        self.progress.stop()
        self.progress.pack_forget()
        self.generate_btn.config(state='normal', text="Generate Report")
        self.status_label.config(text="✗ Error", fg='#C62828')
        messagebox.showerror("Error", f"An error occurred:\n\n{error}")


def main():
    root = tk.Tk()
    
    # Set icon if available
    try:
        root.iconbitmap(default='')
    except:
        pass
    
    app = ReportGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
