import ssl, socket
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")


conn = context.wrap_socket(socket.socket(socket.AF_INET),
                           server_hostname="www.python.org")
conn.connect(("www.python.org", 443))

cert = conn.getpeercert()
pprint.pprint(cert)

conn.sendall(b"HEAD / HTTP/1.0\r\nHost: linuxfr.org\r\n\r\n")
pprint.pprint(conn.recv(1024).split(b"\r\n"))
