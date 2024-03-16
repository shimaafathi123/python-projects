import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from ttkthemes import ThemedTk
import random
import threading
import hashlib

class Peer:
    def __init__(self, username, host, folder_path):
        self.username = username
        self.host = host
        self.folder_path = folder_path

class PeerToPeerNetwork:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Peer-to-Peer Network")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.peers = []
        self.connected_peers = []

        self.create_input_fields()
        self.create_buttons()

        self.selected_receivers = []

    def create_input_fields(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(frame, width=20)
        self.username_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Host:").grid(row=1, column=0, sticky="w")
        self.host_entry = ttk.Entry(frame, width=20)
        self.host_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Select Folder:").grid(row=2, column=0, sticky="w")
        self.folder_path_entry = ttk.Entry(frame, width=20)
        self.folder_path_entry.grid(row=2, column=1)

        self.browse_button = ttk.Button(frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=2, column=2)

        self.sender_var = tk.StringVar(value="Select Sender")
        self.sender_dropdown = ttk.Combobox(frame, textvariable=self.sender_var)
        self.sender_dropdown.grid(row=4, column=1)

        ttk.Label(frame, text="Select Receivers:").grid(row=5, column=0, sticky="w")
        self.receiver_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=3)
        self.receiver_listbox.grid(row=5, column=1)

        ttk.Label(frame, text="Select File:").grid(row=6, column=0, sticky="w")

    def create_buttons(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=1, column=0)

        add_user_button = ttk.Button(frame, text="Add User", command=self.add_peer)
        add_user_button.grid(row=0, column=0)

        send_file_button = ttk.Button(frame, text="Send File", command=self.send_file)
        send_file_button.grid(row=0, column=1)

        request_file_button = ttk.Button(frame, text="Request File", command=self.request_file)
        request_file_button.grid(row=0, column=2)

        view_peers_button = ttk.Button(frame, text="View Peers", command=self.view_peers)
        view_peers_button.grid(row=0, column=3)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)

    def add_peer(self):
        username = self.username_entry.get()
        host = self.host_entry.get()
        folder_path = self.folder_path_entry.get()

        if not (username and host and folder_path):
            messagebox.showwarning("Incomplete Information", "Please provide all required details.")
            return

        if not self.is_valid_host(host):
            messagebox.showwarning("Invalid Host", "Please enter a valid host address.")
            return

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            messagebox.showwarning("Invalid Folder", "Please select a valid folder.")
            return

        if username not in [peer.username for peer in self.connected_peers]:
            peer_folder_path = os.path.join(folder_path, username)
            os.makedirs(peer_folder_path, exist_ok=True)
            
            peer = Peer(username, host, peer_folder_path)
            self.peers.append(peer)
            self.connected_peers.append(peer)
            self.update_sender_receiver_dropdowns()
            self.clear_input_fields()
        else:
            messagebox.showwarning("Duplicate User", "User is already connected.")

    def is_valid_host(self, host):
        # Implement host validation logic based on your requirements
        # For simplicity, a basic check is done here
        return bool(host)

    def send_file(self):
        sender = self.sender_var.get()
        source_file = self.browse_file()

        if not sender or not source_file:
            messagebox.showwarning("Incomplete Information", "Please select sender and file.")
            return

        sender_folder = None
        receiver_folders = []

        for peer in self.peers:
            if peer.username == sender:
                sender_folder = peer.folder_path
            else:
                receiver_folders.append(peer.folder_path)

        if sender_folder and receiver_folders:
            data = self.read_file(source_file)
            if not data:
                return

            chunk_count = len(receiver_folders)
            chunk_size = len(data) // chunk_count

            threads = []
            for i, receiver_folder in enumerate(receiver_folders):
                start = i * chunk_size
                end = start + chunk_size if i < chunk_count - 1 else None
                chunk_data = data[start:end]

                thread = threading.Thread(target=self.write_chunk, args=(receiver_folder, source_file, i, chunk_data))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            os.remove(source_file)

            messagebox.showinfo("File Sent", "File has been divided into chunks and sent to all connected peers except the sender.")

    def read_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            messagebox.showerror("File Read Error", f"Error reading file: {str(e)}")
            return None

    def write_chunk(self, receiver_folder, source_file, i, chunk_data):
        destination_file = os.path.join(receiver_folder, f"chunk_{i}_{os.path.basename(source_file)}")
        try:
            with open(destination_file, 'wb') as chunk_file:
                chunk_file.write(chunk_data)
        except Exception as e:
            messagebox.showerror("File Write Error", f"Error writing chunk: {str(e)}")

    def request_file(self):
        sender = self.sender_var.get()

        if not sender:
            messagebox.showwarning("Incomplete Information", "Please select sender.")
            return

        if not self.selected_receivers:
            self.selected_receivers = [peer.username for peer in self.connected_peers if peer.username != sender]

        for receiver_username in self.selected_receivers:
            sender_peer = next((peer for peer in self.peers if peer.username == sender), None)
            receiver_peer = next((peer for peer in self.peers if peer.username == receiver_username), None)

            if not sender_peer or not receiver_peer:
                messagebox.showwarning("Error", "Sender or receiver not found.")
                return

            self.request_chunks(sender_peer, receiver_peer)

    def request_chunks(self, sender_peer, receiver_peer):
        sender_folder = sender_peer.folder_path
        receiver_folder = receiver_peer.folder_path

        chunk_files = [file for file in os.listdir(receiver_folder) if file.startswith("chunk_")]

        chunks_dict = {}
        for chunk_file in chunk_files:
            chunk_path = os.path.join(receiver_folder, chunk_file)
            chunk_number = int(chunk_file.split("_")[1])
            chunk_data = self.read_file(chunk_path)
            if chunk_data:
                chunks_dict[chunk_number] = chunk_data
                os.remove(chunk_path)

        if chunks_dict:
            original_filename = chunk_files[0].split("_", 2)[-1]
            original_file_path = os.path.join(sender_folder, original_filename)
            with open(original_file_path, 'ab') as original_file:
                for chunk_number in sorted(chunks_dict.keys()):
                    original_file.write(chunks_dict[chunk_number])

            messagebox.showinfo("File Requested", "Chunks have been combined into the original file.")
        else:
            messagebox.showwarning("No Chunks Found", "No chunks were found to combine.")

    def view_peers(self):
        connected_peers_text = tk.Text(self.root, wrap=tk.WORD, width=40, height=10)
        connected_peers_text.grid(row=2, column=0)
        connected_peers_text.config(state=tk.NORMAL)

        shuffled_peers = random.sample(self.connected_peers, len(self.connected_peers))

        connected_peers_text.delete("1.0", tk.END)
        for peer in shuffled_peers:
            connected_peers_text.insert(tk.END, f"Username: {peer.username}\nHost: {peer.host}\nLocation: {peer.folder_path}\n\n")

        connected_peers_text.config(state=tk.DISABLED)

    def clear_input_fields(self):
        self.username_entry.delete(0, tk.END)
        self.host_entry.delete(0, tk.END)
        self.folder_path_entry.delete(0, tk.END)

    def update_sender_receiver_dropdowns(self):
        self.sender_dropdown['values'] = [peer.username for peer in self.connected_peers]
        self.receiver_listbox.delete(0, tk.END)
        for peer in self.connected_peers:
            self.receiver_listbox.insert(tk.END, peer.username)

    def browse_file(self):
        source_file = filedialog.askopenfilename()
        return source_file

if __name__ == "__main__":
    root = ThemedTk(theme="clam")
    app = PeerToPeerNetwork(root)
    root.mainloop()
