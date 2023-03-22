// Three commands to provide new users access to DPdash

// 1.    provide access to studies

db.users.find().forEach(u=>db.users.update({"uid":u.uid}, {$set:{"access": ['ME', 'AD', 'CG', 'JE', 'CP', 'BM', 'ST', 'LS', 'GW', 'SG', 'HK', 'LA', 'OR', 'BI', 'NL', 'NC', 'SD', 'CA', 'YA', 'SF', 'PA', 'SI', 'PI', 'NN', 'IR', 'TE', 'GA', 'WU', 'HA', 'MT', 'KC', 'PV', 'MA', 'CM', 'MU', 'SH', 'SL', 'combined']}}));


// 2.    provide access to configs

[
["Combined - Dataflow",'sbouix'],
["Combined - Forms - Screening",'sbouix'],
["Combined - Forms - Baseline",'sbouix'],
["Combined - Forms - Month1",'sbouix'],
["Combined - Forms - Month 2",'sbouix'],
["Combined - EEG QC",'sbouix'],
["Combined - MRI QC",'sbouix'],
["Combined - Fluid Biomarkers",'sbouix'],
["Combined - Digital Biomarkers",'sbouix'],
["Combined - Audio/Video QC",'sbouix'],
["Digital Biomarker: Mindlamp QC",'sbouix'],
["Digital Biomarker: Axivity+Mindlamp",'sbouix'],
["Individual - Forms",'sbouix'],
["Combined - Forms - Baseline (v.5)",'grace_jacobs'],
["Combined - Forms - Month 1 (v.2)",'grace_jacobs'],
["Combined - Forms - Screening (v.5)",'grace_jacobs']
].forEach(n=> db.configs.update({"name":n[0],'owner':n[1]},{"$set":{"readers": db.users.find().map(u=>u.uid)}}));


// 3.    set default config

db.users.find().forEach(u=>db.users.update({"uid":u.uid}, {$set: {"preferences" : { "complete" : {  }, "star" : {  }, "sort" : 0, "config" : "6415bbd8e0fb897e31326591" }}} ));


