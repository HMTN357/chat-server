import asyncio
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import websockets

class ChatClient:
    def __init__(self, uri, nickname):
        self.uri = uri
        self.nickname = nickname
        self.ws = None

        self.root = tk.Tk()
        self.root.title("WebSocket Chat")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap='word')
        self.text_area.pack(padx=10, pady=10, fill='both', expand=True)
        self.text_area.config(state='disabled')

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill='x', padx=10, pady=5)
        self.entry.bind('<Return>', self.send_message)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    async def connect(self):
        try:
            self.ws = await websockets.connect(self.uri)
            await self.ws.send(f"{self.nickname} joined the chat.")
            asyncio.create_task(self.receive())
        except Exception as e:
            messagebox.showerror("Connection Failed", str(e))
            self.root.destroy()

    async def receive(self):
        try:
            async for msg in self.ws:
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, msg + "\n")
                self.text_area.config(state='disabled')
                self.text_area.yview(tk.END)
        except:
            pass

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            full_msg = f"{self.nickname}: {msg}"
            asyncio.create_task(self.ws.send(full_msg))
            self.entry.delete(0, tk.END)

    def on_close(self):
        if self.ws:
            asyncio.create_task(self.ws.close())
        self.root.destroy()

    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()
    nickname = simpledialog.askstring("Nickname", "Enter your nickname:")
    server_url = simpledialog.askstring("Server URL", "Enter WebSocket URL (e.g., wss://your-app.onrender.com/ws):")
    if not nickname or not server_url:
        return

    client = ChatClient(server_url, nickname)
    asyncio.get_event_loop().run_until_complete(client.connect())
    client.run()

if __name__ == "__main__":
    asyncio.run(main())
