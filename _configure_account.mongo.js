// Three commands to provide new users access to DPdash

// 1.    provide access to studies

db.users.find().forEach(u=>db.users.update({"uid":u.uid}, {$set:{"access": ['ME', 'AD', 'CG', 'JE', 'CP', 'BM', 'ST', 'LS', 'GW', 'SG', 'HK', 'LA', 'OR', 'BI', 'NL', 'NC', 'SD', 'CA', 'YA', 'SF', 'PA', 'SI', 'PI', 'NN', 'IR', 'TE', 'GA', 'WU', 'HA', 'MT', 'KC', 'PV', 'MA', 'CM', 'MU', 'SH', 'SL', 'combined']}}));


// 2.    provide access to configs

[['date-avl-cnb-mriqc-kcho','chief'], ['combined-mriqc','kcho'], ['eegqc-2','speroncire'],['avlqc_combined', 'dpdash'],['subj-formqc-details','grace_jacobs'],['combined-screening-forms','grace_jacobs'],['combined-baseline-forms2','grace_jacobs'],['Digital Biomarker: Axivity+Mindlamp','habibrahimi']].forEach(n=> db.configs.update({"name":n[0],'owner':n[1]},{"$set":{"readers": db.users.find().map(u=>u.uid)}}));


// 3.    set default config

db.users.find().forEach(u=>db.users.update({"uid":u.uid}, {$set: {"preferences" : { "complete" : {  }, "star" : {  }, "sort" : 0, "config" : "635aed24113c5b40ed62fd8d" }}} ));


