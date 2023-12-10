import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64,random
from io import BytesIO
from cleaning import load_data
colors = ['skyblue', 'lightcoral', 'lightgreen', 'lightseagreen', 'lightsalmon', 'lightblue', 'lightpink', 'lightyellow', 'lightgrey', 'lightgreen', 'lightcyan']

def get_image_base64(plt):
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close()
    img_buf.seek(0)
    return base64.b64encode(img_buf.getvalue()).decode('utf-8')


#eda-1
def histogram(filename,column):
    df = load_data(filename)
    plt.figure(figsize=(15, 10))
    plt.hist(df[column], bins=20, edgecolor='black', alpha=0.7, color=random.choice(colors))
    plt.title(f'Histogram of {column}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    return {"plot": get_image_base64(plt)}

#eda-2
def analysis_mean_by(filename,numeric_col,cat_col):
    df = load_data(filename)
    bar_plot = df.groupby(cat_col)[numeric_col].mean().reset_index()
    plt.figure(figsize=(8, 6))
    plt.bar(bar_plot[cat_col], bar_plot[numeric_col], color=colors)
    plt.title(f'Mean {numeric_col} by {cat_col}')
    plt.xlabel(cat_col)
    plt.ylabel(numeric_col)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return {f"plot": get_image_base64(plt)}

#eda-3
def count_plot(filename,col1,col2):
    df = load_data(filename)
    plt.figure(figsize=(10, 6))
    sns.countplot(x=col1, hue=col2, data=df, palette='Set2')
    plt.title(f'{col1} by {col2}')
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.xticks(rotation=45)

    return {f"plot": get_image_base64(plt)}

#eda-4
def heat_map(filename,columns_of_interest):
    df = load_data(filename)
    selected_data = df[columns_of_interest]
    correlation_matrix = selected_data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix Heatmap')

    return {f"plot": get_image_base64(plt)}

#eda-5
def density_graph(filename,col1,col2_numeric):
    df = load_data(filename)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x=col2_numeric, hue=col1, fill=True, common_norm=False, palette='husl')
    plt.title(f'Density of {col1} on {col2_numeric}')
    plt.xlabel(col2_numeric)
    plt.ylabel('Density')
    
    return {f"plot": get_image_base64(plt)}

#eda-6
def piechart(filename,col):
    df = load_data(filename)
    plt.figure(figsize=(10, 5))
    col_counts = df[col].value_counts()
    plt.pie(col_counts, labels=col_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title(col)

    return {f"plot": get_image_base64(plt)}

#eda-7
def scatter_plot(filename,col1,col2_numeric,col3_numeric):
    df = load_data(filename)
    plt.figure(figsize=(12, 6))
    for status, group in df.groupby(col1):
        plt.scatter(group[col2_numeric], group[col3_numeric], label=status)
    plt.title(f'Scatter Plot of {col2_numeric} vs. {col3_numeric} (Colored by {col1})')
    plt.xlabel(col2_numeric)
    plt.ylabel(col3_numeric)
    plt.legend()
   
    return {f"plot": get_image_base64(plt)}

#eda-8
def cross_tab(filename,col1,col2,col3):
    df = load_data(filename)
    cross_tab = pd.crosstab(index=df[col1], columns=[df[col2], df[col3]])
    plt.figure(figsize=(10, 6))
    sns.heatmap(cross_tab, annot=True, cmap='YlGnBu', fmt='d')
    plt.title(f'Relationship between {col1}, {col2}, and {col3}')
    plt.xlabel(f'{col2} & {col3}')
    plt.ylabel(f'{col1}')
    plt.xticks(rotation=45)
   
    return {f"plot": get_image_base64(plt)}
