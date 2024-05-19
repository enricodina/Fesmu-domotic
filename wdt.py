import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import functools

class WDTTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Initialize timers list
        self.timers = []
        self.end_times = []

        # Add widgets for WDT timers
        self.timer_frame = ttk.LabelFrame(self, text="Watchdog Timers")
        self.timer_frame.pack(padx=10, pady=10, fill="both", expand=True)

        for i in range(4):
            # Create labels
            timer_label = ttk.Label(self.timer_frame, text="Timer " + str(i+1) + ":")
            timer_label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            # Create start/reset button
            start_button = ttk.Button(self.timer_frame, text="Start/Reset", command=functools.partial(self.start_timer_dialog, i))
            start_button.grid(row=i, column=2, padx=5, pady=5)

            # Create timer label
            timer_var = tk.StringVar()
            timer_label = ttk.Label(self.timer_frame, textvariable=timer_var)
            timer_label.grid(row=i, column=3, padx=5, pady=5)
            self.timers.append(timer_var)

            # Create event button
            event_button = ttk.Button(self.timer_frame, text="Event", command=functools.partial(self.event_dialog, i))
            event_button.grid(row=i, column=4, padx=5, pady=5)

            # Initialize end time
            self.end_times.append(datetime.now())

        # Update timers every second
        self.update_timers()

    def update_timer(self, label, end_time):
        remaining_time = end_time - datetime.now()
        if remaining_time <= timedelta(seconds=0):
            label.set("00:00:00")
            # Send email when Timer 1 reaches 0
            if label == self.timers[0]:
                self.send_email()
        else:
            remaining_str = str(remaining_time).split(".")[0]
            label.set(remaining_str)

    def start_timer_dialog(self, index):
        # Create a time setup dialog
        time_str = simpledialog.askstring("Timer Setup", f"Enter time for Timer {index + 1} (days hours minutes seconds):")
        if time_str:
            try:
                time_values = [int(val) for val in time_str.split()]
                if len(time_values) >= 4:
                    end_time = datetime.now() + timedelta(days=time_values[0], hours=time_values[1], minutes=time_values[2], seconds=time_values[3])
                    self.timers[index].set(time_str)  # Update timer label with selected time
                    # Update end time in the list
                    self.end_times[index] = end_time
                else:
                    raise ValueError("Incomplete input")
            except ValueError as e:
                print("Error:", e)  # Handle invalid input

    def event_dialog(self, index):
        # Create a dialog for email setup
        origin_email = simpledialog.askstring("Email Setup", "Enter origin email address:")
        if origin_email:
            destination_email = simpledialog.askstring("Email Setup", "Enter destination email address:")
            if destination_email:
                email_title = simpledialog.askstring("Email Setup", "Enter email title:")
                if email_title:
                    file_path = filedialog.askopenfilename(title="Select File to Attach")
                    self.send_email(origin_email, destination_email, email_title, file_path)

    def send_email(self, origin_email="e.codina.v@gmail.com", destination_email="enricodina@hotmail.com", email_title="Timer Alert", file_path=None):
        # Email setup
        email_user = origin_email
        email_password = "warhammer1"
        email_send = destination_email

        subject = email_title

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = f"Timer 1 has reached 0."
        msg.attach(MIMEText(body, 'plain'))

        # Attach file if provided
        if file_path:
            filename = file_path.split('/')[-1]
            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)

        text = msg.as_string()

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()

    def update_timers(self):
        for i, (label, end_time) in enumerate(zip(self.timers, self.end_times)):
            self.update_timer(label, end_time)
        self.after(1000, self.update_timers)
