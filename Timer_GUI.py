import customtkinter as ctk # type: ignore
import database as Time_data
from tkinter import messagebox, filedialog # type: ignore
import os


class TimerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        Time_data.init_db()

        # Window Configuration
        self.title("Timer Settings")
        self.geometry("450x550")

        self.geometry("700x400") 

        # Main Window Grid Configuration
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)    

        # LEFT COLUMN: Inputs & Buttons
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.target_process_label = ctk.CTkLabel(self.left_frame, text="Target Process:")
        self.target_process_label.pack(anchor="w", pady=(0, 5))

        #Create a frame to hold the entry and the browse button side by side
        self.browse_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.browse_frame.pack(anchor="w", pady=(0, 15))

        self.target_process_entry = ctk.CTkEntry(self.browse_frame, width=135)
        self.target_process_entry.pack(side = "left",padx=(0, 5))

        #Browse button to open file dialogue
        self.browse_button = ctk.CTkButton(self.browse_frame, text="Browse", command=self.file_browser, width=60)
        self.browse_button.pack(side = "left")

        self.available_time_label = ctk.CTkLabel(self.left_frame, text="Available Time (minutes):")
        self.available_time_label.pack(anchor="w", pady=(0, 5))

        self.available_time_entry = ctk.CTkEntry(self.left_frame, width=200)
        self.available_time_entry.pack(pady=(0, 25))

        self.save_button = ctk.CTkButton(self.left_frame, text="Save Settings", command=self.save_and_refresh, width=200)
        self.save_button.pack(pady=(0, 10))

        # self.show_button = ctk.CTkButton(self.left_frame, text="Show Current Settings", command=lambda: self.display_current_settings(Time_data.get_data()), width=200)
        # self.show_button.pack()

        self.clear_button = ctk.CTkButton(self.left_frame, text="Remove process", command=self.remove_process, width=200)
        self.clear_button.pack(pady=(10, 0))

        self.clear_button = ctk.CTkButton(self.left_frame, text="Clear Settings", command=self.clear_settings, width=200)
        self.clear_button.pack(pady=(10, 0))

        # RIGHT COLUMN: The Scrollable List
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Currently Tracked Processes")
        self.scrollable_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        self.display_current_settings(Time_data.get_data())


    def save_and_refresh(self):
        self.save_settings()
        self.display_current_settings(Time_data.get_data())
    # Save the settings from the GUI to the database
    def save_settings(self):
        
        target_process = self.target_process_entry.get().strip().lower()
        available_time = self.available_time_entry.get()

        blacklist = ["", " ", "timer_gui.py", "database.py", "python.exe", "pythonw.exe", "ctk.exe", "ctkapp.exe", "cmd.exe", "powershell.exe", "explorer.exe", "taskmgr.exe", "regedit.exe", "timer_gui.exe", "database.exe", "timer settings.exe"]

        if target_process in blacklist:
            messagebox.showerror("Action Blocked","Nice Try")
            return

        for entry in Time_data.get_data():
                    if entry['target_process'] == target_process:
                        Time_data.update_setting(target_process, available_time)
                        messagebox.showinfo("Settings Saved", "Your settings have been saved successfully.")
                        self.target_process_entry.delete(0, ctk.END)
                        return

        try:
            if int(available_time) <= 0:
                messagebox.showerror("Invalid Input", "Available time must be a positive number.")
                return
            else:
                available_time = int(self.available_time_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for available time.")
            return
        
        



        Time_data.update_setting(target_process, available_time)
        messagebox.showinfo("Settings Saved", "Your settings have been saved successfully.")

        self.target_process_entry.delete(0, ctk.END)
        self.available_time_entry.delete(0, ctk.END)
    
    # Display the current settings in the scrollable frame
    def display_current_settings(self, data):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for entry in data:
            card = ctk.CTkFrame(self.scrollable_frame, fg_color="#383838", corner_radius=10)
            card.pack(fill="x", padx=10, pady=5)
            process_info = f"Process: {entry['target_process']} | Time: {entry['gone_time']} / {entry['available_time']} mins"
            label = ctk.CTkLabel(card, text=process_info, font=ctk.CTkFont(weight="bold"))
            label.pack(fill="x", padx=10, pady=5)
    
    # Clear the settings from the database and the GUI
    def clear_settings(self):
        confirm = messagebox.askyesno("Clear Settings", "Are you sure you want to delete all tracked processes? This cannot be undone.")
        if confirm:
            Time_data.clear_settings()
            self.display_current_settings(Time_data.get_data())
            messagebox.showinfo("Settings Cleared", "All settings have been cleared.")
    
    # Remove a specific process from the database and the GUI
    def remove_process(self):
        dialog = ctk.CTkInputDialog(text="Enter the name of the process to remove:", title="Remove Process")
        input_process = dialog.get_input()
        if input_process:
            Time_data.clear_process(input_process)
            self.display_current_settings(Time_data.get_data())
            messagebox.showinfo("Process Removed", f"The process '{input_process}' has been removed from tracking.")
            self.target_process_entry.delete(0, ctk.END)
        elif input_process == "":
            messagebox.showerror("Invalid Input", "Process name cannot be empty. Please enter a valid process name.")
        else:
            return

    # Open a file dialog to select a process executable and populate the target process entry with the selected file name
    def file_browser(self):
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*")])
        if file_path:
            file_name = os.path.basename(file_path)

            self.target_process_entry.delete(0, ctk.END)
            self.target_process_entry.insert(0, file_name)

if __name__ == "__main__":
    app = TimerGUI()
    app.mainloop()