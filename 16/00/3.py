import ssl
context = ssl.SSLContext()
print(context.cert_store_stats())

#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#ctx.set_ciphers('ECDHE+AESGCM:!ECDSA')#ssl.SSLError: ('No cipher can be selected.',)
#ctx.get_ciphers()  # OpenSSL 1.0.x # AttributeError: 'SSLContext' object has no attribute 'get_ciphers'

stats = context.session_stats()
print(stats['hits'], stats['misses'])
