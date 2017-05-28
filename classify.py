#>>>>>>>>          Camera Functions           <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - may of 2017           #
#-------------------------------------------------------#

#from     import svm
from commons import *
from sklearn.svm import SVC
import cPickle as pickle

TESTES = 0.2 # 20% of data for the final test
TRAIN = 'treino.out'


#classify the obj, put a name
def classify(objs):
    
    #load train
    clf = pickle.load(open(TRAIN,'rb'))

    data = []
    for obj in objs:
        data.append(dataLoad(obj))
    
    if data is []:
        return
    nums = clf.predict(data)

    for obj,num in zip(objs,nums):
        obj.name = num2name(num)
        ColorClassify(obj)

#identify all object by a nome
def name2num(name):
    return {
        'cube': 1,
        'sphere': 2, 
        'L':3, 
        'plus':4, 
        'rect':5, 
        'coin':6,
    }[name]

#identify all object by a number
def num2name(num):
    return {
        1:'cube',
        2:'sphere', 
        3:'L', 
        4:'plus', 
        5:'rect', 
        6:'coin',
    }[num]

def ColorClassify(obj):
    if obj.red_per_blue > 1:
        obj.name = 'red '+ obj.name
    else:
        obj.name = 'blue '+ obj.name

#put in a list all attributes of object
def dataLoad(obj):
    data = []
    data.append(obj.area)
    data.append(obj.deform)
    data.append(obj.circle)
    data.append(obj.oblong)
    data.append(obj.perimeter)
    data.append(obj.edges)
    data.append(obj.red_per_blue)
    data.append(obj.out_per_in)

    return data

def train(objs):
    
    # =============== Data

    n_objs = len(objs)
    n_test = toInt(n_objs*TESTES)

    #create a train_data and train_labels
    train_data = []
    train_labels = []

    for obj in objs[:n_objs-n_test]:
        data = dataLoad(obj)

        train_data.append(data)

        train_labels.append(name2num(obj.name))

    #create a list of test
    test_data = []
    test_labels = []
    for obj in objs[n_objs-n_test:]:

        data = dataLoad(obj)

        test_data.append(data)

        test_labels.append(name2num(obj.name))


    # =============== Train
    clf = SVC()
    
    #config
    clf.kernel = 'linear'
    #clf.kernel = 'poly'
    clf.max_iter = 1000000
    clf.tol = 1e-8
    clf.probability = True
    

    #train
    print(clf.fit(train_data, train_labels)) 

    # =============== Result
    
    #print(clf.predict_log_proba(test_data))
    print(clf.predict(test_data))
    print(np.array(test_labels))


    #print(clf.predict_proba(train_data))
    print(clf.predict(train_data))
    print(np.array(train_labels))

    #save train
    pickle.dump( clf, open(TRAIN, 'wb' ) )
