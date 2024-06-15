import socket  # Import modul socket untuk koneksi socket
import select  # Import modul select untuk multiplexing IO
import http.server  # Import modul http.server untuk membuat HTTP server
import urllib.parse  # Import modul urllib.parse untuk parsing URL

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    Penanganan permintaan HTTP untuk proxy yang meneruskan permintaan koneksi CONNECT.

    Metode:
    - do_CONNECT: Menangani permintaan koneksi CONNECT.
    - connect_to_target: Terhubung ke server target untuk permintaan CONNECT.
    - exchange_data: Pertukaran data antara klien dan server target.

    Atribut:
    - self.path: Path atau URL yang diminta oleh klien.
    - self.command: Metode permintaan (CONNECT).
    - self.headers: Header permintaan dari klien.
    - self.connection: Koneksi socket ke klien.
    """

    def do_CONNECT(self):
        """
        Menangani permintaan koneksi CONNECT dari klien.
        """
        self.connect_to_target()

    def connect_to_target(self):
        """
        Terhubung ke server target sesuai dengan permintaan CONNECT dari klien.
        """
        try:
            address = self.path.split(':')  # Memisahkan host dan port dari self.path
            host = address[0]  # Mendapatkan host
            port = int(address[1])  # Mendapatkan port

            # Membuat koneksi ke server target
            soc = socket.create_connection((host, port))

            # Memberi respons ke klien bahwa koneksi berhasil dibuat
            self.send_response(200, 'Connection established')
            self.end_headers()

            # Pertukaran data antara klien dan server target
            self.exchange_data(soc)
        except Exception as e:
            self.send_error(500, str(e))  # Mengirim respons error jika terjadi exception

    def exchange_data(self, soc):
        """
        Melakukan pertukaran data antara klien (melalui self.connection) dan server target (soc).
        """
        try:
            soc.setblocking(0)  # Mengatur socket server agar non-blocking
            self.connection.setblocking(0)  # Mengatur socket klien agar non-blocking

            while True:
                # Memilih socket yang siap untuk dibaca atau ditulis
                read_sockets, _, _ = select.select([self.connection, soc], [], [])

                # Menerima data dari klien dan meneruskannya ke server target
                if self.connection in read_sockets:
                    data = self.connection.recv(4096)
                    if not data:
                        break
                    soc.sendall(data)

                # Menerima data dari server target dan meneruskannya ke klien
                if soc in read_sockets:
                    data = soc.recv(4096)
                    if not data:
                        break
                    self.connection.sendall(data)
        finally:
            soc.close()  # Menutup koneksi socket server
            self.connection.close()  # Menutup koneksi socket klien

def run(server_class=http.server.HTTPServer, handler_class=ProxyHTTPRequestHandler, port=9919):
    """
    Fungsi untuk menjalankan server proxy HTTP pada port yang ditentukan.

    Args:
    - server_class: Kelas server HTTP yang digunakan (default: http.server.HTTPServer).
    - handler_class: Kelas penanganan permintaan HTTP (default: ProxyHTTPRequestHandler).
    - port: Port tempat server proxy HTTP akan berjalan (default: 9919).
    """
    server_address = ('', port)  # Alamat server kosong artinya akan mendengarkan semua antarmuka
    httpd = server_class(server_address, handler_class)
    print(f'Mulai server proxy pada port {port}...')
    httpd.serve_forever()  # Memulai server dan terus berjalan

if __name__ == '__main__':
    run()  # Memanggil fungsi run() jika script ini dijalankan sebagai program utama
