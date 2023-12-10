from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from cleaning import load_data
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, precision_recall_curve, auc, average_precision_score,ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier 
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from eda import get_image_base64

def smote_and_splitting(filename):
    df = load_data(filename)
    le = LabelEncoder()
    for column in df.columns:
        if df[column].dtypes != "float64":
            df[column] = le.fit_transform(df[column])
            df[column] = le.fit_transform(df[column])
    X = df.drop(columns=df.columns[-1])
    y = df[df.columns[-1]]
    smote =  SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y)
    # X_train, X_test, y_train, y_test = 
    return X_resampled,train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

def pre_processsing(X,X_train,X_test):
    scale_cols = []
    for f in X.columns:
        if X[f].max() > 1:
            scale_cols.append(f)
    scale_cols
    scaler = MinMaxScaler()
    #scale only the train set for unbaised model during run with test dataset
    scaler.fit(X_train[scale_cols])
    X_train[scale_cols] = scaler.transform(X_train[scale_cols])
    X_test[scale_cols] = scaler.transform(X_test[scale_cols])
    return X_train,X_test

def build_confusion_matrix(confusion, classes, title='Confusion Matrix', cmap=plt.cm.Oranges,normalized=False):
    plt.figure()
    plt.imshow(confusion, interpolation='nearest', cmap=cmap,)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    threshold = confusion.max() / 2.
    if normalized:
        confusion = confusion.astype('float') / confusion.sum(axis=1)[:, np.newaxis]
        plt.imshow(confusion, interpolation='nearest', cmap=cmap, vmin=0, vmax=1)
    else:
        plt.imshow(confusion, interpolation='nearest', cmap=cmap)
    for i in range(confusion.shape[0]):
        for j in range(confusion.shape[1]):
            plt.text(j, i, confusion[j, i], horizontalalignment="center", color="white" if confusion[i, j] > threshold else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return get_image_base64(plt)

def build_precision_recall_curve(recall,precision,average_precision,title):
    plt.figure()
    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall curve For {0}: AUC={1:0.2f}'.format(title,average_precision))
    return get_image_base64(plt)

#Model-1 KNN

def KNN_algo(filename,k_value):
    X,splitted = smote_and_splitting(filename)
    X_train, X_test, y_train, y_test = splitted
    X_train,X_test = pre_processsing(X,X_train,X_test)
    knn_clf = KNeighborsClassifier(n_neighbors = k_value, metric = 'minkowski', p=2) # Euclidean Distance Metric
    knn_clf.fit(X_train, y_train)
    y_pred = knn_clf.predict(X_test)
    report = classification_report(y_test, y_pred,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    html_report = report_df.to_html()
    report["html_report"] = html_report
    report["train_accuracy"] = f"{accuracy_score(y_train, knn_clf.predict(X_train))*100:.2f}"
    report["test_accuracy"] = f"{accuracy_score(y_test, y_pred)*100:.2f}"
    confusion = confusion_matrix(y_test, y_pred)
    class_names = np.unique(y_test)
    report["confusion_matrix"] =  build_confusion_matrix(confusion, class_names)
    precision, recall, _ = precision_recall_curve(y_test, y_pred)  
    average_precision = average_precision_score(y_test, y_pred)
    report["PR_curve"] = build_precision_recall_curve(recall,precision,average_precision,"KNN")
    def diff_k_values():
        error_rates = []
        accuracies = []
        # Evaluate kNN for different values of k
        for k in range(1,k_value):
            knn = KNeighborsClassifier(n_neighbors=k,metric = 'minkowski', p=2)
            knn.fit(X_train, y_train)
            y_pred = knn.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            accuracies.append(accuracy)
            error_rate = 1 - accuracy
            error_rates.append(error_rate)

        plt.figure(figsize=(10, 6))
        plt.plot(range(1,k_value), error_rates, marker='o', linestyle='-', color='b')
        plt.title('Test Error for Different Values of k in KNN')
        plt.xlabel('Number of Neighbors (k)')
        plt.ylabel('Error Rate')
        return get_image_base64(plt)
    report["k_curve"] = diff_k_values()
    return report

#Model-2 Logistic Regression 
def lgr_algo(filename):
    X,splitted = smote_and_splitting(filename)
    X_train, X_test, y_train, y_test = splitted
    X_train,X_test = pre_processsing(X,X_train,X_test)
    log_regr = LogisticRegression()
    log_regr.fit(X_train, y_train)
    y_pred_lgr = log_regr.predict(X_test)
    report = classification_report(y_test, y_pred_lgr,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report["html_report"] = report_df.to_html()
    report["train_accuracy"] = f"{accuracy_score(y_train, log_regr.predict(X_train))*100:.2f}"
    report["test_accuracy"] = f"{accuracy_score(y_test, y_pred_lgr)*100:.2f}"
    confusion_log_regr = confusion_matrix(y_test, y_pred_lgr)
    class_names = np.unique(y_test)
    report["confusion_matrix"] = build_confusion_matrix(confusion_log_regr, classes=class_names, title='Confusion Matrix For Logistic Regression',cmap=plt.cm.Blues)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_lgr)  
    average_precision = average_precision_score(y_test, y_pred_lgr)

    report["PR_curve"] = build_precision_recall_curve(recall,precision,average_precision,"logistic regression")
    return report

#Model-3 Random Forest Classifier
def random_forest_algo(filename,n_value):
    X,splitted = smote_and_splitting(filename)
    X_train, X_test, y_train, y_test = splitted
    X_train,X_test = pre_processsing(X,X_train,X_test)
    rf_regr = RandomForestClassifier(n_estimators=n_value,min_samples_split=5,random_state=1)
    rf_regr.fit(X_train, y_train)
    y_pred_rf_classifier = rf_regr.predict(X_test)
    report = classification_report(y_test, y_pred_rf_classifier,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report["html_report"] = report_df.to_html()
    report["train_accuracy"] = f"{accuracy_score(y_train, rf_regr.predict(X_train))*100:.2f}"
    report["test_accuracy"] = f"{accuracy_score(y_test, y_pred_rf_classifier)*100:.2f}"
    class_names = np.unique(y_test)
    confusion_rf= confusion_matrix(y_test, y_pred_rf_classifier)
    report["confusion_matrix"] = build_confusion_matrix(confusion_rf, classes=class_names, title='Confusion Matrix for Random Forest Classifier',cmap=plt.cm.Greens)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_rf_classifier)  
    average_precision = average_precision_score(y_test, y_pred_rf_classifier)

    report["PR_curve"] = build_precision_recall_curve(recall,precision,average_precision,"Random Classifier")
    return report
#Model-4 SVC with rbf kernal
def svc_rbf_kernal(filename):
    X,splitted = smote_and_splitting(filename)
    X_train, X_test, y_train, y_test = splitted
    X_train,X_test = pre_processsing(X,X_train,X_test)
    svc_rbf = SVC(kernel = 'rbf', random_state = 0)
    svc_rbf.fit(X_train, y_train)
    y_pred_svc = svc_rbf.predict(X_test)
    report = classification_report(y_test, y_pred_svc,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report["html_report"] = report_df.to_html()
    report["train_accuracy"] = f"{accuracy_score(y_train, svc_rbf.predict(X_train))*100:.2f}"
    report["test_accuracy"] = f"{accuracy_score(y_test, y_pred_svc)*100:.2f}"
    confusion_svc = confusion_matrix(y_test, y_pred_svc)
    class_names = np.unique(y_test)
    report["confusion_matrix"] = build_confusion_matrix(confusion_svc, classes=class_names, title='SVC with rbf kernal',cmap=plt.cm.Reds)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_svc)  
    average_precision = average_precision_score(y_test, y_pred_svc)

    report["PR_curve"] = build_precision_recall_curve(recall,precision,average_precision,"SVC with RBF kernal")
    return report
#Model-5 XGboost
def xgboost_classifier(filename,n_estimators,max_depth):
    X,splitted = smote_and_splitting(filename)
    X_train, X_test, y_train, y_test = splitted
    X_train,X_test = pre_processsing(X,X_train,X_test)
    
    xgboost = XGBClassifier(max_depth=max_depth, learning_rate=0.01, n_estimators=n_estimators, gamma=0, 
                            min_child_weight=1, subsample=0.8, colsample_bytree=0.8, reg_alpha=0.005)
    xgboost.fit(X_train, y_train)
    y_pred_xgboost = xgboost.predict(X_test)
    report = classification_report(y_test, y_pred_xgboost,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report["html_report"] = report_df.to_html()
    report["train_accuracy"] = f"{accuracy_score(y_train, xgboost.predict(X_train))*100:.2f}"
    report["test_accuracy"] = f"{accuracy_score(y_test, y_pred_xgboost)*100:.2f}"
    confusion_xgboost = confusion_matrix(y_test, y_pred_xgboost)
    class_names = np.unique(y_test)
    report["confusion_matrix"]= build_confusion_matrix(confusion_xgboost, classes=class_names, title='Confusion Matrix for XGboost',cmap=plt.cm.BuPu)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_xgboost)  
    average_precision = average_precision_score(y_test, y_pred_xgboost)
    report["PR_curve"] =  build_precision_recall_curve(recall,precision,average_precision,"XGboost")
    return report
   

#Model-6 Gaussian Naive Bayes
def gaussian_classifier(filename):
    X,splitted = smote_and_splitting(filename)
    X_train, X_test, y_train, y_test = splitted
    X_train,X_test = pre_processsing(X,X_train,X_test)
    
    gauss = GaussianNB()
    gauss.fit(X_train, y_train)
    y_pred_nb = gauss.predict(X_test)
    report = classification_report(y_test, y_pred_nb,output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report["html_report"] = report_df.to_html()
    report["train_accuracy"] = f"{accuracy_score(y_train, gauss.predict(X_train))*100:.2f}"
    report["test_accuracy"] = f"{accuracy_score(y_test, y_pred_nb)*100:.2f}"
    confusion_nb = confusion_matrix(y_test, y_pred_nb)
    class_names = np.unique(y_test)
    report["confusion_matrix"] = build_confusion_matrix(confusion_nb, classes=class_names, title='Confusion Matrix for Gaussian Naive Bayes',cmap=plt.cm.PuBuGn)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_nb)  
    average_precision = average_precision_score(y_test, y_pred_nb)

    report["PR_curve"] = build_precision_recall_curve(recall,precision,average_precision,"Gaussian Naive Bayes")
    return report


