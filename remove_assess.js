// javascript code executed by mongo interpreter behind admin authentication

// assess is an array passed to this script

['toc','metadata'].forEach(g=> {
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
        print(db[g].remove({"study":s}));
    })
})
