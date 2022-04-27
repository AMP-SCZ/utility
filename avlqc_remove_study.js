// javascript code executed by mongo interpreter behind admin authentication
// this script accepts an array of "studies"

studies.forEach(s => {

    print(s);

    // delete children collections
    let colls= db.toc.find({"study":s});
    let num= colls.length();

    for (let i=0; i<num; i++) {
            print(db[ colls[i].collection ].remove({}));
    }

    // delete parent collection
    print(db.toc.remove({"study":s}));
})
