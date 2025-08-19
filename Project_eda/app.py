import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def load_data(file_input):
    if isinstance(file_input, pd.DataFrame):
        return file_input            # Already a DataFrame
    
    # Handle Streamlit UploadedFile or local file path
    if hasattr(file_input, "name"):  # Streamlit UploadedFile has a 'name' attribute
        filename = file_input.name.lower()
        if filename.endswith('.csv'):
            try:
                return pd.read_csv(file_input, encoding='utf-8')
            except UnicodeDecodeError:
                return pd.read_csv(file_input, encoding='ISO-8859-1')
        elif filename.endswith('.xlsx'):
            return pd.read_excel(file_input)
        elif filename.endswith('.json'):
            return pd.read_json(file_input)
        else:
            raise ValueError("Unsupported file type. Please upload CSV, Excel, or JSON.")
    
    # Handle string file paths
    if isinstance(file_input, str):
        if file_input.endswith('.csv'):
            try:
                return pd.read_csv(file_input, encoding='utf-8')
            except UnicodeDecodeError:
                return pd.read_csv(file_input, encoding='ISO-8859-1')
        elif file_input.endswith('.xlsx'):
            return pd.read_excel(file_input)
        elif file_input.endswith('.json'):
            return pd.read_json(file_input)
        else:
            raise ValueError("Unsupported file type. Please use CSV, Excel, or JSON.")
    
    raise TypeError("Input must be an uploaded file, file path, or pandas DataFrame.")


# ✅ Show basic info
def basic_info(df, n=5):
    st.subheader("📊 Basic Data Info")
    bool_cols = df.select_dtypes(include=['bool']).columns
    if len(bool_cols) > 0:
        df = df.copy()
        for col in bool_cols:
            df[col] = df[col].replace({True: 'True', False: 'False'})
    st.write(f"Showing {n} rows of your data:")
    st.write(df.head(n))
    st.write(f"**Length of data:** {len(df)}")
    st.write(f"**Shape of data:** {df.shape}")
    st.write("**Data Types:**")
    st.write(df.dtypes)
    st.write("**Columns:**")
    st.write(df.columns.tolist())
    st.write("**Basic Statistics:**")
    st.write(df.describe())
    st.write("**Number of null values in each column:**")
    st.write(df.isnull().sum())


# ✅ Check null values
def check(df):
    nul = False
    st.subheader("🔍 Checking Null Values")
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            st.write(f"NO NULL value in '{col}'")
        else:
            st.write(f"Yes, there are {df[col].isnull().sum()} NULL values in '{col}'")
            nul = True
    return nul


# ✅ Fill missing values
def fill_nu(df, nul):
    if nul: 
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
            else:
                mode_value = df[col].mode()[0]
                df[col].fillna(mode_value, inplace=True)
        st.success("✅ Null values filled successfully.")
    else:
        st.info("No null values found. Nothing to fill.")

    st.write("After filling nulls:")
    st.write(df.isnull().sum())
    return df


# ✅ Auto EDA plots
def auto_eda_plots(df):
    sns.set(style="whitegrid")
    df = df.copy()
    date_cols = []
    
    # Detect date-like columns
    for col in df.select_dtypes(include=['object']).columns:
        try:
            converted = pd.to_datetime(df[col], errors='coerce')
            if converted.notnull().mean() > 0.8:
                date_cols.append(col)
        except:
            pass

    if date_cols:
        st.warning(f"⚠ Excluding date-like columns from plots: {date_cols}")
        df = df.drop(columns=date_cols)

    st.subheader("--- Univariate Analysis ---")
    st.subheader("❌PLEASE NOTE:- If your dataset contains 'Unnamed' columns then it will give Invalid 'Information' and 'Plots'. Please check your dataset.")
    if df.shape[1] == 0:
        st.warning("⚠ No columns available for plotting after filtering.")
        return
         
    for col in df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        if df[col].dtype in ['int64', 'float64']:
            sns.histplot(df[col].dropna(), kde=True, bins=30, ax=ax)
            ax.set_title(f"Histogram of {col}")
        else:
            sns.countplot(x=df[col], order=df[col].value_counts().index, ax=ax)
            ax.set_title(f"Count Plot of {col}")
            plt.xticks(rotation=45)
        st.pyplot(fig)

    st.subheader("--- Bivariate Analysis ---")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object', 'bool', 'category']).columns

    # Numeric vs Numeric (Pairplot)
    if len(numeric_cols) >= 2:
        st.write("### Pair Plot (Numeric vs Numeric)")
        sns.pairplot(df[numeric_cols].dropna())
        st.pyplot(plt.gcf())
        plt.clf()
    else:
        st.info("Not enough numeric columns for Pair Plot.")

    # Numeric vs Categorical (Boxplot)
    if len(numeric_cols) > 0 and len(categorical_cols) > 0:
        for num_col in numeric_cols:
            for cat_col in categorical_cols:
                if df[cat_col].nunique() > 1:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    sns.boxplot(x=df[cat_col], y=df[num_col], ax=ax)
                    ax.set_title(f"Boxplot: {num_col} vs {cat_col}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig, use_container_width=True)
    else:
        st.info("Not enough numeric & categorical columns for Boxplots.")

    # Categorical vs Categorical (Heatmap of counts)
    if len(categorical_cols) >= 2:
        for i in range(len(categorical_cols)):
            for j in range(i+1, len(categorical_cols)):
                crosstab = pd.crosstab(df[categorical_cols[i]], df[categorical_cols[j]])
                if crosstab.shape[0] > 1 and crosstab.shape[1] > 1:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    sns.heatmap(crosstab, annot=True, fmt="d", cmap="Blues", ax=ax)
                    ax.set_title(f"Heatmap: {categorical_cols[i]} vs {categorical_cols[j]}")
                    st.pyplot(fig, use_container_width=True)
    else:
        st.info("Not enough categorical columns for Heatmap.")

    st.subheader("--- Multivariate Analysis ---")
    if len(numeric_cols) > 2:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap (Numeric Features)")
        st.pyplot(fig, use_container_width=True)
    else:
        st.info("Not enough numeric columns for Correlation Heatmap.")
    
def groupby_analysis(df):
    st.subheader("📊 Group By Analysis")
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if len(categorical_cols) == 0 or len(numeric_cols) == 0:
        st.warning("⚠ No categorical or numeric columns available for groupby analysis.")
        return

    group_col = st.selectbox("Select a categorical column to group by:", categorical_cols)
    agg_cols = st.multiselect("Select numeric columns to aggregate:", numeric_cols, default=numeric_cols)
    agg_funcs = st.multiselect("Select aggregation functions:", ['mean', 'sum', 'count', 'median'], default=['mean', 'sum'])

    if st.button("Run GroupBy Analysis"):
        grouped_df = df.groupby(group_col)[agg_cols].agg(agg_funcs)
        st.write("### Grouped Data")
        st.dataframe(grouped_df)

        # Plot grouped data
        for col in agg_cols:
            for func in agg_funcs:
                if (col, func) in grouped_df.columns:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    grouped_df[col][func].plot(kind='bar', ax=ax)
                    ax.set_title(f"{func.title()} of {col} by {group_col}")
                    st.pyplot(fig,use_container_width=True)
    st.success("✅ EDA Plots Completed!")


# ✅ Streamlit App
def main():
    st.title("📂 Data Cleaning & Visualization App")
    
    uploaded_file = st.file_uploader("Upload your file (CSV, Excel, JSON)", type=["csv", "xlsx", "json"])
    
    if uploaded_file:
        df = load_data(uploaded_file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # ✅ Fix Arrow-incompatible dtypes
        for col in df.columns:
            if str(df[col].dtype) == 'Int64':  # Nullable integer
                df[col] = df[col].astype('int64')
            elif str(df[col].dtype) == 'Float64':  # Nullable float
                df[col] = df[col].astype('float64')
            elif str(df[col].dtype) == 'boolean':  # Nullable boolean
                df[col] = df[col].astype('bool')
            elif df[col].dtype == 'object':  # Mixed type
                df[col] = df[col].astype(str)

        if df is not None:
            basic_info(df, 5)
            nul_flag = check(df)
            cleaned_df = fill_nu(df, nul_flag)
            auto_eda_plots(cleaned_df)
            groupby_analysis(cleaned_df)
if __name__ == "__main__":
    main()

