import pandas as pd
from progressbar import *
import os
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# minSupport, minConfigure
minSupport = 0.1
minConfigure = 0.5

property = ['location', 'Area Id', 'beat', 'Priority', 'Incident Type Id', 'Event Number']

# Association_rules
class Rules():
    def __init__(self):
        self.minSupport = minSupport
        self.minConfigure = minConfigure
    # apriori
    def CountApriori(self, Dataset):
        C1 = self.C1Gen(Dataset)
        Dataset = [set(data) for data in Dataset]
        F1, SupRate = self.CkSupportFilter(Dataset, C1)
        F = [F1]
        k = 2
        while len(F[k-2]) > 0:
            Ck = self.ApGen(F[k-2], k) 
            Fk, SupK = self.CkSupportFilter(Dataset, Ck) 
            SupRate.update(SupK)
            F.append(Fk)
            k += 1
        return F, SupRate

    def C1Gen(self, Dataset):
        C1 = []
        progress = ProgressBar()
        for data in progress(Dataset):
            for i in data:
                if [i] not in C1:
                    C1.append([i])
        return [frozenset(i) for i in C1]
    # Ck_low_support_filtering
    def CkSupportFilter(self, Dataset, Ck):
        CompuCk = dict()
        for data in Dataset:
            for cand in Ck:
                if cand.issubset(data):
                    if cand not in CompuCk:
                        CompuCk[cand] = 1
                    else:
                        CompuCk[cand] += 1

        num_items = float(len(Dataset))
        reLi = []
        SupRate = dict()

        for key in CompuCk:
            support  = CompuCk[key] / num_items
            if support >= self.minSupport:
                reLi.insert(0, key)
            SupRate[key] = support
        return reLi, SupRate

    def ApGen(self, Fk, k):
        reLi = []
        Flength = len(Fk)

        for i in range(Flength):
            for j in range(i+1, Flength):
                F1 = list(Fk[i])[:k-2]
                F2 = list(Fk[j])[:k-2]
                F1.sort()
                F2.sort()
                if F1 == F2:
                    reLi.append(Fk[i] | Fk[j])
        return reLi

    def GenRule(self, F, SupRate):
        StroRule = []
        for i in range(1, len(F)):
            for freSet in F[i]:
                H1 = [frozenset([item]) for item in freSet]
                if i > 1:
                    self.RuleItem(freSet, H1, SupRate, StroRule)
                else:
                    self.CountConfigure(freSet, H1, SupRate, StroRule)
        return StroRule

    def RuleItem(self, freSet, H, SupRate, StroRule):
        m = len(H[0])
        if len(freSet) > (m+1):
            p1 = self.ApGen(H, m+1)
            p1 = self.CountConfigure(freSet, p1, SupRate, StroRule)
            if len(p1) > 1:
                self.RuleItem(freSet, p1, SupRate, StroRule)

    def CountConfigure(self, freSet, H, SupRate, StroRule):
        tempH = []
        for item in H:
            sup = SupRate[freSet]
            conf = sup / SupRate[freSet - item]
            lift = conf / SupRate[item]
            jaccard = sup / (SupRate[freSet - item] + SupRate[item] - sup)
            if conf >= self.minConfigure:
                StroRule.append((freSet-item, item, sup, conf, lift, jaccard))
                tempH.append(item)
        return tempH



class CrimeAnalysis():
    def __init__(self):
        self.outputLocation = './results'
        pass

    def LoadData(self):

        Data11 = pd.read_csv("./archive/records-for-2011.csv", encoding="utf-8")
        Data12 = pd.read_csv("./archive/records-for-2012.csv", encoding="utf-8")
        Data13 = pd.read_csv("./archive/records-for-2013.csv", encoding="utf-8")
        Data14 = pd.read_csv("./archive/records-for-2014.csv", encoding="utf-8")
        Data15 = pd.read_csv("./archive/records-for-2015.csv", encoding="utf-8")
        Data16 = pd.read_csv("./archive/records-for-2016.csv", encoding="utf-8")


        Data12.rename(columns={"Location 1": "Location"}, inplace = True)
        Data13.rename(columns={"Location ": "Location"}, inplace = True)
        Data14.rename(columns={"Location 1": "Location"}, inplace = True)

        Data11_temp = Data11[["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]]
        Data12_temp = Data12[["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]]
        Data13_temp = Data13[["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]]
        Data14_temp = Data14[["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]]
        Data15_temp = Data15[["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]]
        Data16_temp = Data16[["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]]

        AllData = pd.concat([Data11_temp, Data12_temp, Data13_temp, Data14_temp, Data15_temp, Data16_temp],
                             axis=0)
        print(" ", AllData.columns)
        AllData = AllData.dropna(how='any')

        return AllData.head(10000)
        #return AllData


    def Mine(self, property):
            out_path = self.outputLocation
            association = Rules()

            AllData = self.LoadData()
            rows = AllData.values.tolist()

            Dataset = []
            propertys = ["Agency", "Location", "Area Id", "Beat", "Priority", "Incident Type Id", "Incident Type Description", "Event Number"]
            for data_line in rows:
                data_set = []
                for i, value in enumerate(data_line):
                    if not value:
                        data_set.append((propertys[i], 'NA'))
                    else:
                        data_set.append((propertys[i], value))
                Dataset.append(data_set)


            freSet, SupRate = association.CountApriori(Dataset)
            SupRate_out = sorted(SupRate.items(), key=lambda d: d[1], reverse=True)
            print("SupRate ", SupRate)

            StroRule = association.GenRule(freSet, SupRate)
            StroRule = sorted(StroRule, key=lambda x: x[3], reverse=True)
            print("StroRule ", StroRule)

            FreFile = open(os.path.join(out_path, 'freq.json'), 'w')
            for (key, value) in SupRate_out:
                ReDic = {'set': None, 'sup': None}
                SetRe = list(key)
                SupRe = value
                if SupRe < minSupport:
                    continue
                ReDic['set'] = SetRe
                ReDic['sup'] = SupRe
                strJson = json.dumps(ReDic, ensure_ascii=False)
                FreFile.write(strJson + '\n')
            FreFile.close()

            RuleFile = open(os.path.join(out_path, 'rules.json'), 'w')
            for result in StroRule:
                ReDic = {'X_set': None, 'Y_set': None, 'sup': None, 'conf': None, 'lift': None, 'jaccard': None}
                X_set, Y_set, sup, conf, lift, jaccard = result
                ReDic['X_set'] = list(X_set)
                ReDic['Y_set'] = list(Y_set)
                ReDic['sup'] = sup
                ReDic['conf'] = conf
                ReDic['lift'] = lift
                ReDic['jaccard'] = jaccard

                strJson = json.dumps(ReDic, ensure_ascii=False)
                RuleFile.write(strJson + '\n')
            RuleFile.close()

if __name__ == "__main__":
    CrimeAnalysis().Mine(property)