# Safe Cleanup and Archive

Archive generated evidence before cleanup.

```bash
mkdir -p archive/$(date +%Y%m%d)
cp -a reports archive/$(date +%Y%m%d)/reports-snapshot
```

Never archive private keys, tokens, credentials, or raw production evidence.
