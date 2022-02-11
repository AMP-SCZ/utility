from hashlib import hash

assessment='flowcheck'

with open('combined_metadata.csv') as f:
    ids=f.read().split('\n')

ids= [i for i in ids if i]
    
for i in ids:
    e= i.split(',')
    name= e[-1]+ e[0]+ assessment
    hashes.append(sha256(name.encode()).hexdigest())
