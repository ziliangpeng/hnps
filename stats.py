import leveldb

db = leveldb.LevelDB('./algolia')

print db.GetStats()
