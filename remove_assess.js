// javascript code executed by mongo interpreter behind admin authentication

// assess is an array or a string passed to this script

// when it is a string, obtain the list of assessments
if (assess[0].length==1) {
    let _assess=[]
    db.toc.find().forEach(s=>s.basename.match(assess) && _assess.push(s.assessment))
    assess=[ ... new Set(_assess)]
}

assess.forEach(s => {

    print(s);

    // delete children collections
    let colls= db.toc.find({"assessment":s});
    let num= colls.length();

    for (let i=0; i<num; i++) {
        db[ colls[i].collection ].drop();
        db.adminCommand({ flushRouterConfig: colls[i].collection })
    }


    // delete parent collection
    db.toc.deleteMany({"assessment":s});

})


