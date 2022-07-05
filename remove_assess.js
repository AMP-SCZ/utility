// javascript code executed by mongo interpreter behind admin authentication

// assess is an array or a string passed to this script

// when it is a string, obtain the list of assessments
if (assess[0].length==1) {
    let _assess=[]
    db.toc.find().forEach(s=>s.basename.match(assess) && _assess.push(s.assessment))
    assess=[ ... new Set(_assess)]
}

['toc'].forEach(g=> {
    print('Removing',g)

    assess.forEach(s => {

        print(s);

        // delete children collections
        let colls= db[g].find({"assessment":s});
        let num= colls.length();

        for (let i=0; i<num; i++) {
                print(db[ colls[i].collection ].remove({}));
        }

        // delete parent collection
        print(db[g].remove({"assessment":s}));
    })
})
