import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def load_data(filepath):
    return pd.read_csv(filepath)

def save_data(df,filepath):
    return df.to_csv(filepath, index=False)

def get_head(filepath):
    df = load_data(filepath)
    return df.head().to_json()


def get_columns(filepath,type="cat"):
    df = load_data(filepath)
    if type=="cat":
        return df.columns
    else:
        return df.select_dtypes(include=['int64', 'float64']).columns




#cleaning -1
def get_missing_data(filepath):
    df = load_data(filepath)
    missing_values = df.isnull().sum()
    missing_values_percentage = (df.isnull().sum() / df.shape[0]) * 100
    missing_df = pd.DataFrame({'Total Missing Values': missing_values, 'Percentage': missing_values_percentage})

    plt.figure(figsize=(10, 14))
    missing_df['Percentage'].plot(kind='barh')
    plt.xlabel('Percentage (%)')
    plt.ylabel('Features')
    plt.title('Percentage of Missing Values by Feature')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close()
    img_buf.seek(0)

    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    save_data(df,filepath)
    return {"missing_data": missing_df.to_dict(), "plot_image": img_base64}

#cleaning -2
def remove_null(filepath):
    df = load_data(filepath)
    res = df.isnull().sum().to_dict()
    df.dropna(inplace=True)
    save_data(df,filepath)
    return  res
    

#cleaning -3
def remove_duplicate(filepath):
    df = load_data(filepath)
    df.duplicated().any()
    df.drop_duplicates(inplace=True)
    save_data(df,filepath)
    return True

#cleaning -4
def drop_cols(filepath,columns):
    if len(columns) == 0:
        return {"status":"No columns Dropped!"}
    df = load_data(filepath)
    df.drop(columns=columns,inplace=True)
    save_data(df,filepath)
    return {"status":f"{columns} Dropped!"}

#cleaning -5
def imputation_of_missing_values(filepath):
    df = load_data(filepath)
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    all_columns = set(df.columns)
    numerical_columns_set = set(numerical_cols)
    for column in numerical_cols:
        df[column].fillna(int(df[column].mean()), inplace=True)
    remaining_cols = list(all_columns - numerical_columns_set)
    for column in remaining_cols:
        df[column].fillna(df[column].mode()[0], inplace=True)
    df.dropna(inplace=True)
    missing_values = df.isnull().sum()
    missing_values_percentage = (df.isnull().sum() / df.shape[0]) * 100
    missing_df = pd.DataFrame({'Total Missing Values': missing_values, 'Percentage': missing_values_percentage})
    save_data(df,filepath)
    return missing_df.to_dict()

#cleaning-6
def get_datatypes(filepath):
    df = load_data(filepath)
    return df.dtypes.astype(str).to_dict()

#cleaning-7
def renaming_columns(filepath,new_columns):
    df = load_data(filepath)
    df.rename(columns=new_columns, inplace=True)
    save_data(df,filepath)
    return new_columns

#cleaning-8
def data_trimming(filepath,numeric_cols):
    df = load_data(filepath)
    for column in numeric_cols:
        bottom_threshold = df[column].quantile(0.02)
        top_threshold = df[column].quantile(0.98)
        df = df[(df[column] >= bottom_threshold) & (df[column] <= top_threshold)]
    save_data(df,filepath)
    return df.head().to_html()

#cleaning-9
def describe_data(filepath):
    df = load_data(filepath)
    return df.describe().to_html()

#cleaning-10
def box_blot_outliers(filepath,numeric_cols):
    df = pd.read_csv(filepath)
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(numeric_cols):
        plt.subplot(3, 3, i + 1)
        plt.boxplot(df[col].dropna())
        plt.title(col)
    plt.tight_layout()

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close()
    img_buf.seek(0)

    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    outliers_info = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_limit) | (df[col] > upper_limit)]
        outliers_info[col] = len(outliers)

    return {"boxplot_image": img_base64, "outliers": outliers_info}