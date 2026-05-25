import psutil # type: ignore
from datetime import date
import database
import tkinter as tk # type: ignore


def main():

    # Create a transparent overlay window that will display the remaining time for each tracked process
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    root.title("Time left")
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "black")
    root.configure(bg='black')
    root.geometry(f"300x150+{screen_width - 320}+20")

    overlay_label = tk.Label(root, text="", font=("Consolas", 14, "bold"), fg="#00CA00", bg="black", justify="right")
    overlay_label.pack(anchor="ne")


    session_seconds = {}

    # Function to kill a process by name
    def kill_process(process_name):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                try:
                    proc.kill()
                except psutil.AccessDenied:
                    pass

    # Function to check running processes against the database and update usage time, kill processes that exceed their limits, and reset usage time daily
    #It also updates the overlay with remaining time information.
    def main_check():

        try:
            data = database.get_data()
            today_date = date.today().isoformat()
            running_process = []
            time_left_info = ""

            # Get a list of currently running processes
            for proc in psutil.process_iter(['name']):
                if proc.info['name']:
                    running_process.append(proc.info['name'].lower())
        
            for dat in data:
                target_process = dat["target_process"].lower()
                available_time = dat["available_time"]
                gone_time = dat["gone_time"]
                last_date = dat["date"]

                #Reset gone time to 0 if the date has changed since the last update for that process
                if last_date != today_date:
                    gone_time = 0
                    database.update_usage(gone_time, today_date, target_process)
                    session_seconds[target_process] = 0

                # If the target process is running, calculate remaining time and kill it if it has exceeded the available time. Otherwise, update the overlay with the remaining time information.
                if target_process in running_process:
                    if target_process not in session_seconds:
                        session_seconds[target_process] = 0

                    total_available_seconds = available_time * 60
                    total_gone_seconds = (gone_time * 60) + session_seconds[target_process]
                    remaining_seconds = total_available_seconds - total_gone_seconds

                    if  remaining_seconds <= 0:
                        kill_process(target_process)
                        database.update_usage(available_time, today_date, target_process)
                        session_seconds[target_process] = 0
                    else:
                        session_seconds[target_process] += 1

                        if session_seconds[target_process] >= 60:
                            gone_time += 1
                            database.update_usage(gone_time, today_date, target_process)
                            session_seconds[target_process] = 0

                    minutes_left = remaining_seconds // 60
                    seconds_left = remaining_seconds % 60

                    time_left_info += f"{target_process}: {minutes_left}m {seconds_left}s\n"

            overlay_label.config(text=time_left_info.strip()) 

        except Exception as e:
            print(f"An error occurred: {e}")
    
        root.after(1000, main_check)  # Schedule the next check each second even if there's an error
    main_check()
    root.mainloop()


if __name__ == "__main__":
    main()