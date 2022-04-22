// javascript code executed by mongo interpreter behind admin authentication

use dpdata;
studies= [... new Set(db.toc.find().map(s=> s.study))]
use dpdmongo;
db.users.update({"uid":uid}, {$set: {"access": studies}})

