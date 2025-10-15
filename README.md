# 📊 E-commerce Revenue Drop Analysis & Dashboard

## 🎯 Project Goal
This project aims to analyse e-commerce sales data to uncover valuable insights, such as top-selling products, revenue trends, and customer purchasing behaviour. Additionally, an **interactive Streamlit dashboard** is built to allow dynamic exploration of the dataset.

## ✅ Outcomes
- **Data Cleaning & Preprocessing:** Fixed missing values, standardised formats, and calculated total revenue.
- **Exploratory Data Analysis (EDA):** Identified best-selling products, peak sales periods, and revenue distribution.
- **Visualizations:** Used Matplotlib and Seaborn to create meaningful charts.
- **Interactive Dashboard:** Developed with Streamlit, featuring:
  - **Sales trends over time**
  - **Best-selling products analysis**
  - **Revenue breakdown by category**
  - **Dynamic filtering for product categories**

## 🛠️ Technologies Used
- **Python** (Pandas, NumPy, Matplotlib, Seaborn)
- **Streamlit** (for dashboard visualization)
- **Jupyter Notebook** (for exploratory data analysis)
- **Excel & OpenPyXL** (for dataset handling)

## 📂 Project Structure
```
📁 ecommerce-dashboard/
│── 📁 data/                 # Raw dataset
│    ├── ecommerce_sales.xlsx
│── 📁 notebooks/            # Jupyter Notebook analysis
│    ├── ecommerce_analysis.ipynb
│── 📁 dashboard/            # Streamlit app
│    ├── dashboard.py
│── requirements.txt         # Dependencies
│── LICENSE                  # View-only license
│── README.md                # Project documentation
```

## 🚀 How to Run Locally
1. **Clone the repository:**
```sh
git clone https://github.com/mayhemds/ecommerce-dashboard.git
cd ecommerce-dashboard
```
2. **Install dependencies:**
```sh
pip install -r requirements.txt
```
3. **Run the Streamlit dashboard:**
```sh
streamlit run dashboard/dashboard.py
```




