import numpy as np

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

for _ in range(10):
    org_list = np.array([np.random.random() for i in range(100)])
    # print(org_list)
    est_list = np.array([org_list[i] + 5 * np.random.random() for i in range(100)])
    # print(est_list)
    new_list = do_compare(org_list, est_list)
    # print(new_list)
    orgTwoNorm = 0
    twoNorm = 0
    for i in range(len(new_list)):
        orgTwoNorm += np.square(est_list[i] - org_list[i])
        twoNorm += np.square(new_list[i] - org_list[i])
    orgTwoNorm = np.sqrt(orgTwoNorm)
    twoNorm = np.sqrt(twoNorm)
    print(orgTwoNorm, twoNorm, orgTwoNorm > twoNorm)