import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ByCS Serienmail")
        
        # Konfiguration
        self.config = {
            "owa_username": "",
            "owa_password": "",
            "owa_url": "",
            "csv_file": "",
            "attachment_folder": "",
            "subject": "",
            "body_template": ""
        }

        # Erstellen der Benutzeroberfläche
        self.create_widgets()
        self.update_start_button_state()
        
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="ByCS Benutzername:").grid(row=0, column=0, sticky=tk.W)
        self.owa_username_entry = ttk.Entry(frame, width=50)
        self.owa_username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.owa_username_entry.bind("<KeyRelease>", self.update_start_button_state)

        ttk.Label(frame, text="ByCS Passwort:").grid(row=1, column=0, sticky=tk.W)
        self.owa_password_entry = ttk.Entry(frame, width=50, show='*')
        self.owa_password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.owa_password_entry.bind("<KeyRelease>", self.update_start_button_state)

        ttk.Label(frame, text="OWA URL:").grid(row=2, column=0, sticky=tk.W)
        self.owa_url_entry = ttk.Entry(frame, width=50)
        self.owa_url_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.owa_url_entry.insert(0, "https://mail.schule.bayern.de/owa")
        self.owa_url_entry.bind("<KeyRelease>", self.update_start_button_state)

        ttk.Label(frame, text="CSV-Datei Empfänger:").grid(row=3, column=0, sticky=tk.W)
        self.csv_entry = ttk.Entry(frame, width=50)
        self.csv_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))
        self.csv_entry.bind("<KeyRelease>", self.update_start_button_state)
        ttk.Button(frame, text="Browse...", command=self.browse_csv).grid(row=3, column=2)

        ttk.Label(frame, text="Ordner mit Anhängen:").grid(row=4, column=0, sticky=tk.W)
        self.attachment_entry = ttk.Entry(frame, width=50)
        self.attachment_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Browse...", command=self.browse_folder).grid(row=4, column=2)

        ttk.Label(frame, text="Betreff:").grid(row=5, column=0, sticky=tk.W)
        self.subject_entry = ttk.Entry(frame, width=50)
        self.subject_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))
        self.subject_entry.bind("<KeyRelease>", self.update_start_button_state)

        ttk.Label(frame, text="Text der E-Mail:").grid(row=6, column=0, sticky=tk.W)
        self.body_entry = tk.Text(frame, width=50, height=10)
        self.body_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))
        self.body_entry.bind("<KeyRelease>", self.update_start_button_state)

        self.start_button = ttk.Button(frame, text="Start", command=self.start_sending_emails, state=tk.DISABLED)
        self.start_button.grid(row=7, column=0, columnspan=3)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=8, column=0, columnspan=3, pady=10)

        for child in frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def update_start_button_state(self, event=None):
        all_fields_filled = (
            self.owa_username_entry.get() and
            self.owa_password_entry.get() and
            self.owa_url_entry.get() and
            self.csv_entry.get() and
            self.subject_entry.get() and
            self.body_entry.get("1.0", tk.END).strip()
        )
        if all_fields_filled:
            self.start_button.state(['!disabled'])
        else:
            self.start_button.state(['disabled'])

    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, file_path)
            self.update_start_button_state()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.attachment_entry.delete(0, tk.END)
            self.attachment_entry.insert(0, folder_path)

    def start_sending_emails(self):
        # Speichern der Konfiguration aus den Eingabefeldern
        self.config['owa_username'] = self.owa_username_entry.get()
        self.config['owa_password'] = self.owa_password_entry.get()
        self.config['owa_url'] = self.owa_url_entry.get()
        self.config['csv_file'] = self.csv_entry.get()
        self.config['attachment_folder'] = self.attachment_entry.get()
        self.config['subject'] = self.subject_entry.get()
        self.config['body_template'] = self.body_entry.get("1.0", tk.END)

        # Starte E-Mail-Versand
        self.send_emails()

    def send_emails(self):
        try:
            df = pd.read_csv(self.config['csv_file'], delimiter=';', encoding='utf-8')
            total_emails = len(df)
            self.progress['maximum'] = total_emails

            driver = webdriver.Chrome()
            driver.get(self.config['owa_url'])
            time.sleep(5)

            # Anmelden
            username = driver.find_element(By.ID, 'input-username')
            username.send_keys(self.config['owa_username'])
            password = driver.find_element(By.ID, 'input-password')
            password.send_keys(self.config['owa_password'])
            password.send_keys(Keys.RETURN)
            time.sleep(5)

            # Eventuelle 2-Faktor-Authentifizierung behandeln
            # ...

            for index, row in df.iterrows():
                # Klick auf "Neue Nachricht"
                new_email_button = driver.find_element(By.CSS_SELECTOR, 'button._fce_h._fce_f.ms-fwt-r.ms-fcl-np.o365button')
                new_email_button.click()
                time.sleep(5)

                # Empfänger eintragen
                to_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="An"]')
                to_field.send_keys(row['Email'])

                # Tab-Taste senden, um zum Betreff-Feld zu wechseln
                to_field.send_keys(Keys.TAB)
                time.sleep(1)

                # Betreff eintragen
                subject_field = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Betreff,"]')
                subject_field.send_keys(self.config['subject'])
                time.sleep(1)

                # Nachrichtentext eintragen
                body_field = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Nachrichtentext"]')
                body_text = self.config['body_template'].format(Vorname=row['Vorname'], Nachname=row['Nachname'])
                
                # Zeilenumbrüche im Nachrichtentext durch <br> ersetzen
                body_text = body_text.replace('\n', '<br>')

                # Finde das erste <p>-Element und füge den Nachrichtentext dort ein
                p_element = body_field.find_element(By.TAG_NAME, 'p')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", p_element, body_text)

                if self.config['attachment_folder']:
                    # Anhänge hinzufügen
                    attachment_filename = f"{row['Vorname']}.{row['Nachname']}.pdf"
                    attachment_path = os.path.join(self.config['attachment_folder'], attachment_filename)
                    if os.path.isfile(attachment_path):
                        attach_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Einfügen"]')
                        attach_button.click()
                        time.sleep(1)
                        
                        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                        file_input.send_keys(attachment_path)
                        time.sleep(5)

                # E-Mail senden
                send_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Senden"]')
                send_button.click()
                time.sleep(5)

                # Update progress bar
                self.progress['value'] = index + 1
                self.root.update_idletasks()

            driver.quit()
            messagebox.showinfo("Erfolgsmeldung", "Alle E-Mails wurden erfolgreich gesendet!")
            root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()
