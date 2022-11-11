import numpy as np
from sklearn.isotonic import IsotonicRegression
import matplotlib.pyplot as plt
import seaborn as sns

def istonic_compare(org_list, est_list):
    iso_reg = IsotonicRegression().fit(org_list, est_list)
    return iso_reg.predict(org_list)

def ask_question(a, b, org_list):
    if org_list[a] > org_list[b]:
        return 0
    else:
        return 1

def do_compare(org_list, est_list):
    new_list = []
    for i in range(len(org_list)):
        new_value = 0
        for j in range(len(org_list)):
            if j == i:
                pass
            elif ask_question(i, j, org_list) == ask_question(i, j, est_list):
                new_value += est_list[i] / (len(est_list) - 1)
            else:
                new_value += (est_list[i] + est_list[j]) / (2 * (len(est_list) - 1))
        new_list.append(new_value)
    return new_list

maxOrg, minOrg, avgOrg = [], [], []
maxOur, minOur, avgOur = [], [], []
maxIstonic, minIstonic, avgIstonic = [], [], []
for j in range(10):
    orgTwoNormList = []
    twoNormList = []
    twoNormIstonicList = []
    for _ in range(100):
        org_list = np.array([np.random.random() for i in range(50)])
        # print(org_list)
        est_list = np.array([org_list[i] + np.power(np.sqrt(2), j-3) * np.random.randn() for i in range(50)])
        # print(est_list)
        new_list = do_compare(org_list, est_list)
        new_list_istonic = istonic_compare(org_list, est_list)
        # print(new_list)
        orgTwoNorm = 0
        twoNorm = 0
        twoNormIstonic = 0
        for i in range(len(new_list)):
            orgTwoNorm += np.square(est_list[i] - org_list[i])
            twoNorm += np.square(new_list[i] - org_list[i])
            twoNormIstonic += np.square(new_list_istonic[i] - org_list[i])
        orgTwoNorm = np.sqrt(orgTwoNorm)
        twoNorm = np.sqrt(twoNorm)
        twoNormIstonic = np.sqrt(twoNormIstonic)
        orgTwoNormList.append(orgTwoNorm)
        twoNormList.append(twoNorm)
        twoNormIstonicList.append(twoNormIstonic)
        # print(orgTwoNorm, twoNorm, twoNormIstonic, orgTwoNorm >= twoNorm)
    maxOrg.append(max(orgTwoNormList))
    minOrg.append(min(orgTwoNormList))
    avgOrg.append(sum(orgTwoNormList)/len(orgTwoNormList))
    maxOur.append(max(twoNormList))
    minOur.append(min(twoNormList))
    avgOur.append(sum(twoNormList)/len(twoNormList))
    maxIstonic.append(max(twoNormIstonicList))
    minIstonic.append(min(twoNormIstonicList))
    avgIstonic.append(sum(twoNormIstonicList)/len(twoNormIstonicList))

plt.rcParams['figure.figsize'] = (10.0, 7.0)
clrs = sns.color_palette("husl", 7)
plt.scatter(np.arange(10)-3, avgOrg, marker='+', label="Two Norm Loss of Original Estimation", c=clrs[0])
plt.scatter(np.arange(10)-3, avgOur, marker='o', label="Two Norm Loss of Our Mechanism", c=clrs[1])
plt.scatter(np.arange(10)-3, avgOur, marker='o', label="Two Norm Loss of Istonic Mechanism", c=clrs[2])
plt.plot(np.arange(10)-3, avgOrg, c=clrs[0])
plt.plot(np.arange(10)-3, avgOur, c=clrs[1])
plt.plot(np.arange(10)-3, avgIstonic, c=clrs[2])
plt.fill_between(np.arange(10)-3, minOrg, maxOrg, alpha=0.3, facecolor=clrs[0])
plt.fill_between(np.arange(10)-3, minOur, maxOur, alpha=0.3, facecolor=clrs[1])
plt.fill_between(np.arange(10)-3, minIstonic, maxIstonic, alpha=0.3, facecolor=clrs[2])
plt.xlabel(r"Variance of Noises (after take $\log_2$)")
plt.ylabel("Two Norm Loss")
plt.legend()
plt.show()
