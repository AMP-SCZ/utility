let hashes= cat(hash_script).split('\n')

hashes.forEach(h => {
    if (h) {
        print(h)
        print(db[h].remove({}))
    }
})


