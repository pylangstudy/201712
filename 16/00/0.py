import ssl
cert = {'subject': ((('commonName', 'example.com'),),)}
ssl.match_hostname(cert, "example.com")
ssl.match_hostname(cert, "example.org") #ssl.CertificateError: hostname 'example.org' doesn't match 'example.com'
