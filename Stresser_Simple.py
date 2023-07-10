import tkinter as tk
from tkinter import ttk
import threading
import requests

class StressTesterGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Website Stress Tester")

        self.label_url = ttk.Label(window, text="URL:")
        self.label_url.pack()

        self.entry_url = ttk.Entry(window)
        self.entry_url.pack()

        self.label_threads = ttk.Label(window, text="Number of Threads:")
        self.label_threads.pack()

        self.entry_threads = ttk.Entry(window)
        self.entry_threads.pack()

        self.label_requests = ttk.Label(window, text="Requests per Thread:")
        self.label_requests.pack()

        self.entry_requests = ttk.Entry(window)
        self.entry_requests.pack()

        self.button_start = ttk.Button(window, text="Start Stress Test", command=self.start_stress_test)
        self.button_start.pack()

        self.result_label = ttk.Label(window, text="")
        self.result_label.pack()

    def start_stress_test(self):
        url = self.entry_url.get()
        threads = int(self.entry_threads.get())
        requests_per_thread = int(self.entry_requests.get())

        if not url or not threads or not requests_per_thread:
            self.result_label.config(text="Please enter valid input.")
            return

        stress_tester = StressTester(url, threads, requests_per_thread)
        stress_tester.run_test()
        self.result_label.config(text="Stress test completed.")

class StressTester:
    def __init__(self, url, threads=10, requests_per_thread=10):
        self.url = url
        self.threads = threads
        self.requests_per_thread = requests_per_thread

    def run_test(self):
        print(f"Running stress test on {self.url} with {self.threads} threads and {self.requests_per_thread} requests per thread.")

        # Create a lock to synchronize the printing of results
        lock = threading.Lock()

        # Create a list to store the threads
        threads = []

        # Create and start the threads
        for _ in range(self.threads):
            thread = threading.Thread(target=self.make_requests, args=(lock,))
            thread.start()
            threads.append(thread)

        # Wait for all the threads to finish
        for thread in threads:
            thread.join()

    def make_requests(self, lock):
        for _ in range(self.requests_per_thread):
            try:
                response = requests.get(self.url)
                with lock:
                    print(f"Thread {threading.current_thread().name}: Response status code - {response.status_code}")
            except requests.exceptions.RequestException as e:
                with lock:
                    print(f"Thread {threading.current_thread().name}: Error - {str(e)}")

# Create the main window
window = tk.Tk()

# Create a StressTesterGUI instance
gui = StressTesterGUI(window)

# Start the main event loop
window.mainloop()
