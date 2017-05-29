#>>>>>>>>          Camera Functions           <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - may of 2017           #
#-------------------------------------------------------#

#from     import svm
from commons import *
from sklearn.svm import SVC
from sklearn import preprocessing
import cPickle as pickle

TESTES = 0.2 # 20% of data for the final test
TRAIN = 'treino.out'


#classify the obj, put a name
def classify(objs):
    
    #load train
    if runOnRasp(): 
        clf,scale = pickle.load(open(TRAIN,'rb'))
    else:
        clf,scale = pickle.load(open('p'+TRAIN,'rb'))

    #data of objs
    data = []
    for obj in objs:
        data.append(dataLoad(obj))

    data = scale.transform(data)

    if data is []:
        return

    #classify
    nums = clf.predict(data)#obj

    for obj,num in zip(objs,nums):#color
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
    data.append(obj.center_per_int)
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

    #scale the data
    scale = preprocessing.MinMaxScaler()
    train_data = scale.fit_transform(train_data)
    test_data = scale.transform(test_data)

    # =============== Train
    clf = SVC()
    
    #config
    #It must be one of 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed' 
    clf.kernel = 'rbf'
    clf.max_iter = 100000
    #clf.degree = 10
    clf.gamma = 10
    clf.tol = 1e-8
    clf.probability = True
    

    #Train
    print(clf.fit(train_data, train_labels)) 

    # =============== Result
    
    erro = np.mean( clf.predict(test_data) != np.array(test_labels))
    print('Erro test: '+str(erro))

    erro = np.mean( clf.predict(train_data) != np.array(train_labels))
    print('Erro Train: '+str(erro))

    #save train
    if runOnRasp(): 
        pickle.dump( [clf,scale], open(TRAIN, 'wb' ) )
    else:
        pickle.dump( [clf,scale], open('p'+TRAIN, 'wb' ) )
