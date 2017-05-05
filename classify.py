#>>>>>>>>          Camera Functions           <<<<<<<<<<#
#        Cordeiro Libel - UTFPR - may of 2017           #
#-------------------------------------------------------#

#identify all object by a number
def name2num(name):
    return {
        'red cube': 1,
        'red sphere': 2,
        'red L':3,
        'red plus':4,
        'blue cube':5,
        'blue sphere':6,
        'blue L':7,
        'blue plus':8,
    }[name]


def train(objs):

    #hog = cv2.HOGDescriptor(winSize)
    #descriptor = hog.compute(im)

    #create a trainData and trainLabels
    trainData = []
    for obj in objs:
        data = []
        data.append(obj.area)
        data.append(obj.deform)
        data.append(obj.circle)
        data.append(obj.oblong)
        data.append(obj.perimeter)
        data.append(obj.red_per_blue)
        data.append(obj.out_per_in)

        trainData.append(data)

        trainLabels.append(name2num(obj.name))

    # Set up SVM for OpenCV 3
    svm = cv2.ml.SVM_create()
    # Set SVM type
    svm.setType(cv2.ml.SVM_C_SVC)
    # Set SVM Kernel to Radial Basis Function (RBF) 
    svm.setKernel(cv2.ml.SVM_RBF)
    # Set parameter C
    svm.setC(12.5)
    # Set parameter Gamma
    svm.setGamma(0.50625)
     
    # Train SVM on training data  
    svm.train(trainData, cv2.ml.ROW_SAMPLE, trainLabels)
     
    # Save trained model 
    svm->save("digits_svm_model.yml");
     
    # Test on a held out test set
    testResponse = svm.predict(testData)[1].ravel()
