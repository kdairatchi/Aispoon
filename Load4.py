import os
import openai
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
import subprocess

# Replace with your own OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

class ZeroDayAutomationTool:
    def __init__(self, master):
        self.master = master
        self.master.title("AI-Powered Zero-Day Automation Tool")
        self.master.geometry("800x600")

        self.label = tk.Label(master, text="Zero-Day Automation Tool for Bug Bounties", font=("Arial", 16))
        self.label.pack(pady=10)

        self.input_label = tk.Label(master, text="Enter your prompt or action request:")
        self.input_label.pack()

        self.user_input = tk.Entry(master, width=100)
        self.user_input.pack(pady=10)

        self.run_button = tk.Button(master, text="Run AI Command", command=self.process_prompt, width=25, bg="green", fg="white")
        self.run_button.pack(pady=10)

        self.output_label = tk.Label(master, text="AI Generated Code/Response:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=95, height=20)
        self.output_text.pack(padx=10, pady=10)

    def process_prompt(self):
        prompt = self.user_input.get()
        if not prompt:
            messagebox.showwarning("Input Error", "Please enter a prompt.")
            return

        # Call GPT-4 or similar to get a response
        ai_response = self.generate_code_from_ai(prompt)

        if ai_response:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, ai_response)

            # Offer the user to execute the code if it's a script
            if "script" in prompt.lower() or "exploit" in prompt.lower():
                execute = messagebox.askyesno("Execute Code", "Would you like to execute the generated code?")
                if execute:
                    self.execute_generated_code(ai_response)

    def generate_code_from_ai(self, prompt):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate response from AI: {str(e)}")
            return ""

    def execute_generated_code(self, code):
        # Save the code to a temporary file
        temp_filename = "temp_script.py"
        try:
            with open(temp_filename, "w") as file:
                file.write(code)
            # Execute the generated script
            subprocess.run(["python", temp_filename], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Execution Error", f"An error occurred during script execution: {str(e)}")
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroDayAutomationTool(root)
    root.mainloop()
