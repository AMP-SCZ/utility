// javascript code executed by mongo interpreter behind admin authentication

// https://www.mongodb.com/docs/manual/tutorial/write-scripts-for-the-mongo-shell/

// use dpdata;
db= db.getSiblingDB('dpdata')
studies= [... new Set(db.toc.find().map(s=> s.study))]
print(studies)

// use dpdmongo;
db= db.getSiblingDB('dpdmongo')
print(db.users.update({"uid": uid}, {$set: {"access": studies}}))

