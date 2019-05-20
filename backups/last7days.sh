# Store only backups of last 7 days and delete older files
find /your-backups-dir -type f -mtime +7 -exec rm -rf {} \;
