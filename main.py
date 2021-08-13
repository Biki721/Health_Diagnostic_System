import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import login
import GUI


data = pd.read_csv('Database/dataset.csv')
df = pd.DataFrame(data)

cols = df.columns[:-1]

ll = list(cols)

pp = []

for i in ll:
    pp.append(str(i))

x = df[cols]  # x is the feature
y = df['prognosis']  # y is the target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

features = cols
feature_dict = {}

latest_features = list(features).copy()

for i, f in enumerate(features):
    feature_dict[f] = i

trix = dict()

for item in latest_features:
    trix[str(item).title().replace('_', ' ')] = item

diseases = []
def prediction():
    # symptoms = ['joint_pain', 'muscle_wasting']
    symptoms = [GUI.p.get(), GUI.en.get(), GUI.bb.get(), GUI.ee.get(), GUI.hh.get()]

    symptoms = [trix[j] for j in symptoms if j != '']

    hack_set = set()
    
    pos = []

    for i in range(len(symptoms)):
        pos.append(feature_dict[symptoms[i]])

    sample_x = [1.0 if i in pos else 0.0 for i in range(len(features))]
    sample_x = [sample_x]
    
    
    #Algorithms
#-----------------------------------------------------------------------------
    # Decision Tree

    dt = DecisionTreeClassifier()

    dt.fit(x_train, y_train)

    print(dt.predict(sample_x))
    print(f"Decision Tree: {dt.predict(sample_x)}")
    
    hack_set.add(*map(str, dt.predict(sample_x)))
    
    diseases.append(dt.predict(sample_x))
    
    DT = dt.predict(sample_x)
    
    y_pred = dt.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    #plt.scatter(y_test[:10],y_pred[:10])
    #plt.show()
    
    print(f"Accuracy Decision Tree: {accuracy * 100}%")
    
    
#-----------------------------------------------------------------------------
    # Naive Bayes

    naive = GaussianNB()

    naive.fit(x_train, y_train)

    print(f"Naive Bayes: {naive.predict(sample_x)}")

    NB = naive.predict(sample_x)

    hack_set.add(*map(str, naive.predict(sample_x)))

    
    y_pred = naive.predict(x_test)

    accuracy_naive = accuracy_score(y_test, y_pred) * 100
    #print('probability',naive.predict_proba(x_test))
    #print(f"Accuracy for Naive Bayes: {accuracy_naive}%")
    
#-----------------------------------------------------------------------------
    # Random Forest

    random = RandomForestClassifier()

    random.fit(x_train, y_train)

    hack_set.add(*map(str, random.predict(sample_x)))

    #diseases.append(random.predict(sample_x))

    print(f"Random Forest: {random.predict(sample_x)}")

    y_pred = random.predict(x_test)

    accuracy_random = accuracy_score(y_test, y_pred) * 100

    #print(f"Accuracy for Random Forest: {accuracy_random}%")
    
#-----------------------------------------------------------------------------

    # LogisticRegression
    Logic = LogisticRegression()

    Logic.fit(x_train, y_train)

    hack_set.add((map(str, Logic.predict(sample_x))))
    
    diseases.append(Logic.predict(sample_x))

    LR = Logic.predict(sample_x)

    print(f'LogisticRegression: {Logic.predict(sample_x)}')

    y_pred = Logic.predict(x_test)
    
    accuracy = accuracy_score(y_test, y_pred)

    #print(f"Accuracy for Logistic Regression: {accuracy * 100}%")
    
#-----------------------------------------------------------------------------

    # SVM

    Svm = svm.SVC()

    Svm.fit(x_train, y_train)
    
    hack_set.add((map(str, Svm.predict(sample_x))))

    #diseases.append(Svm.predict(sample_x))

    y_pred = Svm.predict(x_test)
       
    print(f"SVM: {Svm.predict(sample_x)}")

    accuracy = accuracy_score(y_test, y_pred) * 100

    #print(f"Accuracy for SVM: {accuracy}%")

#-----------------------------------------------------------------------------

    knn = KNeighborsClassifier(n_neighbors=3)
    
    knn.fit(x_train, y_train)
    
    hack_set.add((map(str, knn.predict(sample_x))))
    
    diseases.append(knn.predict(sample_x))

    KN = knn.predict(sample_x)
    
    y_pred = knn.predict(x_test)
    
    print(f"KNN: {knn.predict(sample_x)}")

    accuracy = accuracy_score(y_test, y_pred) * 100
    
    #print(f"Accuracy for KNN: {accuracy}%")

#-----------------------------------------------------------------------------
    magic = list(hack_set)
    
    #print(hack_set)
    print(diseases)
    '''
    s = ""
    if len(hack_set) == 1:
        s = s + "".join(magic[0])
    else:
        s = s + "".join(magic[0]) + ' or ' + "".join(magic[1])
    '''
    # Exceptions for Wrong Try
    
    if not symptoms:
        GUI.final_result1.delete(0, GUI.END)
        GUI.final_result1.insert(0, "Invalid ! No Disease Found")
        
        GUI.final_result2.delete(0, GUI.END)
        GUI.final_result2.insert(0, "Invalid ! No Disease Found")
        
        GUI.final_result3.delete(0, GUI.END)
        GUI.final_result3.insert(0, "Invalid ! No Disease Found")

    elif len(set(symptoms)) != len(symptoms):
        GUI.final_result1.delete(0, GUI.END)
        GUI.final_result1.insert(0, "Invalid ! Try with unique Symptoms")
        
        GUI.final_result2.delete(0, GUI.END)
        GUI.final_result2.insert(0, "Invalid ! Try with unique Symptoms")
        
        GUI.final_result3.delete(0, GUI.END)
        GUI.final_result3.insert(0, "Invalid ! Try with unique Symptoms")
    else:
        GUI.final_result1.delete(0, GUI.END)
        GUI.final_result1.insert(0, DT)
        
        GUI.final_result2.delete(0, GUI.END)
        GUI.final_result2.insert(0, LR)
        
        GUI.final_result3.delete(0, GUI.END)
        GUI.final_result3.insert(0, KN)


def output_name(iter):
    max_num = diseases.count(diseases[0])

    for i in range(len(diseases)-1):
        if  diseases.count(diseases[i+1])> max_num:
            max_num = diseases.count(diseases[i+1])
    return max_num

def final_disease():
    for ds in diseases:
            if diseases.count(ds) == output_name(diseases):
                print(ds)
                break
    return ds

