import http.server
import socketserver
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

HOST = ""
PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/templates/index.html"
        elif self.path == "/about":
            self.path = "/templates/about.html"
        elif self.path == "/contact":
            self.path = "/templates/contact.html"
        elif self.path == "/service":
            self.path = "/templates/service.html"
        elif self.path == "/blog":
            self.path = "/templates/blog.html"
        else:
            self.path=='/templates/blog.html'
            print(self.send_error(404, "Page not found"))
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)# ... Your existing code for handling routes ...

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, ".", recursive=True)
        self.observer.start()
        try:
            run_server()
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type in ['modified', 'created', 'deleted']:
            print(f"Changes detected: {event.src_path}")
            # Restart the server when changes are detected
            os.system("pkill -f 'python server.py'")
            os.system("python server.py")

def run_server():
    os.chdir(os.path.dirname(__file__))
    with socketserver.TCPServer((HOST, PORT), MyHandler) as server:
        print(f"Serving at {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    watcher = Watcher()
    watcher.run()
