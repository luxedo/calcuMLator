import argparse, importlib, json, sys, pickle
#from sklearn import datasets

parser = argparse.ArgumentParser(description='Runs scilit-zero server')
parser.add_argument('--module',  help='Module from sklearn')
parser.add_argument('--method', help='Method')
parser.add_argument('--field', help='Field')
parser.add_argument('--predict', help='Predict', action='store_true')
args = parser.parse_args()

if args.predict:
    pickledModel = ''
    for chunk in sys.stdin:
        if chunk == '\n':
            break
        else:
            pickledModel += chunk
    model = pickle.loads(pickledModel) 
    for chunk in sys.stdin:
        feature = json.loads(chunk)
        label = model.predict(feature)
        sys.stdout.write(json.dumps(label.tolist()))

if args.module:
    moduleName = 'sklearn.' + args.module
    module = importlib.import_module(moduleName)
    method = getattr(module, args.method)

    if (moduleName == 'sklearn.datasets'):
        line = sys.stdin.readline()
        params = json.loads(line)
        data = method(**params)
        field = getattr(data, args.field)
        sys.stdout.write(json.dumps(field.tolist()))
    if (moduleName == 'sklearn.svm'):
        line = sys.stdin.readline()
        params = json.loads(line)
        clf = method(**params)
        featuresList = []
        labelList    = []
        for item in sys.stdin:
            pair = json.loads(item)
            features = pair[0]
            label    = pair[1]
            featuresList.append(features)
            labelList.append(label)
        model = clf.fit(featuresList, labelList)
        pickled = pickle.dumps(model)
        sys.stdout.write(pickled)
        #print(pickled)
