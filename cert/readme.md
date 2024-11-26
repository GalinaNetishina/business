```bash
openssl genrsa -out jwt-private.pem 1024
```

```bash
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```