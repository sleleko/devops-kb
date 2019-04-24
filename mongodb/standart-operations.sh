# dumping database with name exmpdb
mongodump -d exmpdb

# restoring database with name exmpdb
mongorestore -d exmpdb

# if old database exist (old db will dropped before dump restore)
mongorestore --drop -d exmpdb

# if your dump not in standart dir 
mongorestore --drop -d exmpdb dump/exmpdb
