import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    model1= train_model1(X_train, y_train)
    predictions1 = model1.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)
    sensitivity1, specificity1 = evaluate(y_test, predictions1)
    # Print results
    print("k=1")
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    print("svm")
    print(f"Correct: {(y_test == predictions1).sum()}")
    print(f"Incorrect: {(y_test != predictions1).sum()}")
    print(f"True Positive Rate: {100 * sensitivity1:.2f}%")
    print(f"True Negative Rate: {100 * specificity1:.2f}%")

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    mon_index= ["Jan", "Feb", "Mar", "April", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    name= filename
    with open(name) as f:
        reader = csv.reader(f)
        next(reader)

        data = []
        for row in reader:
            li=[]
            i=0
            while i<17:
                if i==0 or i==2 or i==4 or i==11 or i== 12 or i==13 or i==14:
                    li.append(int(row[i]))
                elif i==1 or i==3 or i==5 or i==6 or i==7 or i==8 or i==9:
                    li.append(float(row[i]))
                elif i==10:
                    li.append(mon_index.index(row[i]))
                elif i==15:
                    if row[i]== "Returning_Visitor":
                        li.append(1)
                    else:
                        li.append(0)
                elif i==16:
                    if row[i]== "TRUE":
                        li.append(1)
                    else:
                        li.append(0)
                i+=1

            data.append({
                "evidence": li,
                "label": 0 if row[17] == "FALSE" else 1
            })

    # Separate data into training and testing groups
    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]
    return (evidence, labels)
    raise NotImplementedError

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model= KNeighborsClassifier(n_neighbors= 1)
    return model.fit(evidence, labels)
    
    raise NotImplementedError

def train_model1(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model= svm.SVC()
    return model.fit(evidence, labels)
    
    raise NotImplementedError

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive=0
    positive_id=0
    negative=0
    negative_id=0
    for actual, predicted in zip(labels, predictions):
        if actual== 1:
            positive+= 1
            if actual == predicted:
                positive_id += 1
        else:
            negative+= 1
            if actual == predicted:
                negative_id += 1
    sens= positive_id/positive
    spec= negative_id/negative
    print(positive_id)
    print(positive)
    return(sens, spec)


if __name__ == "__main__":
    main()
