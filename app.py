from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

host_name = "localhost"
server_port = 8080


class TemplateFileHandler:

    @staticmethod
    def read_template_file():
        with open("contacts.html", "r", encoding="UTF-8") as file:
            html_data = file.read()
            return html_data


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        filehandler = TemplateFileHandler()
        html_file = filehandler.read_template_file()
        query_data = parse_qs(urlparse(self.path).query)
        page_content = html_file
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get('content-length'))
        form_data = self.rfile.read(content_length)
        form_fields = parse_qs(str(form_data, "utf-8"))
        print(form_fields)
        self.do_GET()


if __name__ == "__main__":
    web_server = HTTPServer((host_name, server_port), Server)
    print(f"Сервер запущен http://{host_name}:{server_port}")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Сервер остановлен")
