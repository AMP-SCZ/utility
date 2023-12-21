// Three commands to provide new users access to DPdash

let _users;
if (typeof user === 'undefined'){
    _users=db.users.find()
}
else {
    _users=[db.users.findOne({"mail":user})];
}


// 1.    provide access to studies

_users.forEach(u=>db.users.update({"uid":u.uid}, {$set:{"access": ['ME', 'AD', 'CG', 'JE', 'CP', 'BM', 'ST', 'LS', 'GW', 'SG', 'HK', 'LA', 'OR', 'BI', 'NL', 'NC', 'SD', 'CA', 'YA', 'SF', 'PA', 'SI', 'PI', 'NN', 'IR', 'TE', 'GA', 'WU', 'HA', 'MT', 'KC', 'PV', 'MA', 'CM', 'MU', 'SH', 'SL', 'combined']}}));


// 2.    provide access to configs

[
["Combined - Baseline+Month 2 - Dataflow",'chief'],
["Combined - Forms - Month 2",'sbouix'],
["Combined - EEG QC",'sbouix'],
["Combined - MRI QC",'sbouix'],
["Combined - Fluid Biomarkers",'sbouix'],
["Combined - Audio/Video QC",'sbouix'],
["Digital Biomarker: Combined Axivity+Mindlamp for QC (Yearly)",'habibrahimi']
["Digital Biomarker: Axivity+Mindlamp for QC (Daily)",'habibrahimi'],
["Digital Biomarker: Axivity Data for QC (Monthly)",'habibrahimi'],
["Digital Biomarker: Mindlamp Data for QC (Monthly)",'habibrahimi'],
["Individual - Forms",'sbouix'],
["Combined - Forms - Baseline (v.5)",'grace_jacobs'],
["Combined - Forms - Month 1 (v.2)",'grace_jacobs'],
["Combined - Forms - Screening (v.5)",'grace_jacobs']
].forEach(n=> db.configs.update({"name":n[0],'owner':n[1]},{"$set":{"readers": db.users.find().map(u=>u.uid)}}));


// 3.    set default config

_users.forEach(u=>db.users.update({"uid":u.uid}, {$set: {"preferences" : { "complete" : {  }, "star" : {  }, "sort" : 0, "config" : "644848513a2446cb3c1ba4e1" }}} ));


