import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class PayloadRepositoryBuilder:
    def __init__(self, master):
        self.master = master
        self.master.title("Payload Repository Builder with Auto-Updater")
        self.master.geometry("800x700")
        self.structure = {}

        # Labels, buttons, and text area for GUI setup
        self.label = tk.Label(master, text="Payload Repository Builder with Auto-Updater", font=("Arial", 16))
        self.label.pack(pady=10)

        self.add_folder_button = tk.Button(master, text="Add Folder", command=self.add_folder, width=30)
        self.add_folder_button.pack(pady=5)

        self.add_file_button = tk.Button(master, text="Add File", command=self.add_file, width=30)
        self.add_file_button.pack(pady=5)

        self.generate_button = tk.Button(master, text="Generate Repository", command=self.generate_repository, width=30, bg="green", fg="white")
        self.generate_button.pack(pady=10)

        self.update_button = tk.Button(master, text="Update Payloads", command=self.update_payloads, width=30, bg="blue", fg="white")
        self.update_button.pack(pady=10)

        self.structure_display = tk.Text(master, wrap="word", height=20, width=80)
        self.structure_display.pack(padx=10, pady=10)

    def add_folder(self):
        folder_name = simpledialog.askstring("Input", "Enter Folder Name:")
        if folder_name:
            if folder_name not in self.structure:
                self.structure[folder_name] = {}
                self.update_structure_display()
            else:
                messagebox.showwarning("Warning", "Folder already exists.")

    def add_file(self):
        if not self.structure:
            messagebox.showwarning("Warning", "Please add a folder first.")
            return
        folder_name = simpledialog.askstring("Input", "Enter the Folder Name to add the file:")
        if folder_name in self.structure:
            file_name = simpledialog.askstring("Input", "Enter File Name:")
            file_content = simpledialog.askstring("Input", "Enter File Content (optional):")
            if file_name:
                self.structure[folder_name][file_name] = file_content if file_content else ""
                self.update_structure_display()
        else:
            messagebox.showerror("Error", "Folder not found. Please add the folder first.")

    def update_structure_display(self):
        self.structure_display.delete(1.0, tk.END)
        for folder, files in self.structure.items():
            self.structure_display.insert(tk.END, f"Folder: {folder}\n")
            for file, content in files.items():
                self.structure_display.insert(tk.END, f"  ├── File: {file}\n")

    def generate_repository(self):
        base_path = filedialog.askdirectory()
        if not base_path:
            messagebox.showerror("Error", "No directory selected.")
            return

        self.create_repository_structure(base_path, self.structure)
        messagebox.showinfo("Success", f"Repository structure created at: {base_path}")

    def create_repository_structure(self, base_path, structure):
        for folder, files in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file_name, content in files.items():
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "w") as f:
                    f.write(content)

    def update_payloads(self):
        payload_sources = [
            "https://www.exploit-db.com",          # Example vulnerability site
            "https://cve.mitre.org",               # Trusted CVE source
            "https://www.hackerone.com/hacktivity",# HackerOne vulnerability disclosure
            "https://portswigger.net/web-security",# PortSwigger's Web Security Academy
        ]
        new_payloads = self.scrape_payloads(payload_sources)
        if new_payloads:
            for payload_type, payload_content in new_payloads.items():
                if payload_type not in self.structure:
                    self.structure[payload_type] = {}
                file_name = f"updated_{payload_type}_payloads_{datetime.now().strftime('%Y-%m-%d')}.txt"
                self.structure[payload_type][file_name] = payload_content
            self.update_structure_display()
            messagebox.showinfo("Update Complete", "Payloads have been updated.")

    def scrape_payloads(self, sources):
        new_payloads = {}
        try:
            for source in sources:
                response = requests.get(source)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    if "exploit-db" in source:
                        # Extract exploit links or text for Exploit-DB
                        links = soup.find_all('a', class_='exploit_list_item')
                        for link in links:
                            new_payloads["general"] = new_payloads.get("general", "") + link.text.strip() + "\n"

                    elif "cve.mitre" in source:
                        # Extract CVE information
                        tables = soup.find_all('table')
                        for table in tables:
                            rows = table.find_all('tr')
                            for row in rows:
                                if row.find('a'):
                                    cve_text = row.find('a').text.strip()
                                    new_payloads["CVE"] = new_payloads.get("CVE", "") + cve_text + "\n"

                    elif "hackerone" in source:
                        # Extract HackerOne findings
                        issues = soup.find_all('a', class_='title')
                        for issue in issues:
                            new_payloads["general"] = new_payloads.get("general", "") + issue.text.strip() + "\n"

                    elif "portswigger" in source:
                        # Extract payload examples from PortSwigger's website
                        articles = soup.find_all('a', class_='Article-link')
                        for article in articles:
                            new_payloads["PortSwigger"] = new_payloads.get("PortSwigger", "") + article.text.strip() + "\n"

        except requests.RequestException as e:
            messagebox.showerror("Network Error", f"Error fetching data: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during scraping: {str(e)}")
        
        return new_payloads

if __name__ == "__main__":
    root = tk.Tk()
    app = PayloadRepositoryBuilder(root)
    root.mainloop()
