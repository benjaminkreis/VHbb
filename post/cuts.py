cuts=[{} for i in range(10)]

jetPt_cut   = 'hJet_ptCorr[0]>20 && hJet_ptCorr[1]>20'
jetEta_cut  = 'abs(hJet_eta[0]) < 2.4 && abs(hJet_eta[1])<2.4'
jetpuID_cut = 'hJet_puJetIdL[0]>0 && hJet_puJetIdL[1]>0'
hbhe_cut    = 'hbhe'
bad_pixels = '(!(207883<=EVENT.run && EVENT.run<=208307))'

json       = 'EVENT.json==1'
higgsFlag  = 'H.HiggsFlag==1'
trigger    = '( ( Vtype==1 && (triggerFlags[5]>0 || triggerFlags[6]>0) ) || ( Vtype==0 && ( triggerFlags[22]>0 || triggerFlags[23]>0 || triggerFlags[14]>0 || triggerFlags[21]>0 ) ) )'

preselection = jetPt_cut + ' && ' + jetEta_cut + ' && ' + hbhe_cut + ' && ' + jetpuID_cut + ' && ' + bad_pixels + ' && ' + json + ' && ' + higgsFlag + ' && ' + trigger

CSVT = '0.898'
CSVL = '0.244'
CSVC = '0.5'

noAddJet = 'Sum$(aJet_pt > 20 && abs(aJet_eta) < 2.4) == 0'
max1AddJet = 'Sum$(aJet_pt > 20 && abs(aJet_eta) < 2.4) < 2.'

zWindow = 'V.mass > 75. && V.mass < 105'
zVeto =  '(V.mass > 105 || V.mass < 75.)'
looseHMass = 'h_HmCorr > 40. && h_HmCorr < 250.'#'H.mass > 40. && H.mass < 250.'
upperHMass = 'h_HmCorr < 250.'#'H.mass < 250.'
vetoHMass = '(h_HmCorr < 90. || h_HmCorr > 145.)'#'(H.mass < 90. || H.mass > 145.)'
dPhiVH = 'abs(HVdPhi) > 2.9'
twoCSV0 = 'hJet_csvCorr[0] > 0. && hJet_csvCorr[1] > 0.'
pullAngle = 'deltaPullAngle < 10. && deltaPullAngle2 < 10.'

rMed = 'V.pt > 50. && V.pt < 100.'
rTight = 'V.pt > 100.' 

minBtag = 'min(hJet_csvCorr[0],hJet_csvCorr[1])'
maxBtag = 'max(hJet_csvCorr[0],hJet_csvCorr[1])'

tcBtag = maxBtag + ' > ' + CSVT + ' && ' + minBtag + ' > ' + CSVC
ntBtag = '(hJet_csvCorr[0] > ' + CSVT + ' || hJet_csvCorr[1] > ' + CSVT + ')'

cuts[1]['ZLight']= preselection + ' && ' + noAddJet + ' && ' + zWindow + ' && ' + ntBtag + ' && ' + upperHMass + ' && ' + twoCSV0 + ' && ' + dPhiVH + ' && ' + maxBtag + ' > ' + CSVL + ' && V.pt > 50.' + ' && Vtype == 1' # ee
cuts[0]['ZLight']= preselection + ' && ' + noAddJet + ' && ' + zWindow + ' && ' + ntBtag + ' && ' + upperHMass + ' && ' + twoCSV0 + ' && ' + dPhiVH + ' && ' + maxBtag + ' > ' + CSVL + ' && V.pt > 50.' + ' && Vtype == 0' # mumu
cuts[1]['TTbar'] = preselection + ' && ' + upperHMass + ' && ' + tcBtag + ' && ' + zVeto + ' && H.pt > 100.' + ' && Vtype == 1'
cuts[0]['TTbar'] = preselection + ' && ' + upperHMass + ' && ' + tcBtag + ' && ' + zVeto + ' && H.pt > 100.' + ' && Vtype == 0'
cuts[1]['Zbb']   = preselection + ' && ' + vetoHMass + ' && ' + upperHMass + ' && ' + zWindow + ' && ' + tcBtag + ' && ' + max1AddJet + ' && ' + dPhiVH + ' && Vtype == 1'
cuts[0]['Zbb']   = preselection + ' && ' + vetoHMass + ' && ' + upperHMass + ' && ' + zWindow + ' && ' + tcBtag + ' && ' + max1AddJet + ' && ' + dPhiVH + ' && Vtype == 0'
cuts[1]['bdt']   = preselection + ' && (( V.pt < 100 && ' + maxBtag + ' > ' + CSVC + ')||( V.pt > 100 && ' + maxBtag + ' > ' + CSVL + ')) && ' + minBtag + ' > ' + CSVL + ' && ' + zWindow + ' && ' + pullAngle + ' && Vtype == 1'
cuts[0]['bdt']   = preselection + ' && (( V.pt < 100 &&' + maxBtag + ' > ' + CSVC + ')||( V.pt > 100 && ' + maxBtag + ' > ' + CSVL + ')) && ' + minBtag + ' > ' + CSVL + ' && ' + zWindow + ' && ' + pullAngle + ' && Vtype == 0'

