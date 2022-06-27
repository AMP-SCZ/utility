// javascript code executed by mongo interpreter behind admin authentication

// all sites and pseudo sites: PRoNET, PRESCIENT, files
let sites= ['ME', 'AD', 'CG', 'JE', 'CP', 'BM', 'AM', 'LS', 'GW', 'SG', 'HK', 'LA', 'OR', 'BI', 'NL', 'NC', 'SD', 'CA', 'YA', 'SF', 'PA', 'SI', 'PI', 'NN', 'IR', 'TE', 'GA', 'WU', 'HA', 'MT', 'KC', 'PV', 'MA', 'CM', 'MU', 'SH', 'SL', 'ST'].concat(["ProNET", "PRESCIENT", "files"]);

['toc','metadata'].forEach(g=> {
    print('Removing',g)

    sites.forEach(s => {

        print(s);

        // delete children collections
        let colls= db[g].find({"study":s});
        let num= colls.length();

        for (let i=0; i<num; i++) {
                print(db[ colls[i].collection ].remove({}));
        }

        // delete parent collection
        print(db[g].remove({"study":s}));
    })
})
