import pandas as pd
import os

INPUT_FILE = "notebooks/freelancer_earnings_bd.csv"

# Загрузка
df = pd.read_csv(INPUT_FILE)

# Расчёт дополнительных метрик
df["Earnings_per_Project"] = df["Earnings_USD"] / df["Job_Completed"]
df["Is_Expert"] = df["Experience_Level"].str.lower() == "expert"

# Классификация по регионам
region_map = {
    "United States": "North America",
    "Canada": "North America",
    "Germany": "Europe",
    "France": "Europe",
    "India": "Asia",
    "Philippines": "Asia",
    "Brazil": "South America",
    "Argentina": "South America",
}
df["Region_Short"] = df["Client_Region"].map(region_map).fillna("Other")

# Бины по количеству завершённых работ
df["Job_Range_Label"] = pd.cut(
    df["Job_Completed"],
    bins=[-1, 9, 99, float("inf")],
    labels=["<10", "10–99", "100+"]
)

# Бины по почасовой ставке
df["Hourly_Band"] = pd.cut(
    df["Hourly_Rate"],
    bins=[-1, 10, 30, float("inf")],
    labels=["<10$", "10$–30$", "30$+"]
)

# Топ-25% по доходу
q75 = df["Earnings_USD"].quantile(0.75)
df["High_Earner"] = df["Earnings_USD"] > q75

# Классификация клиентов по рейтингу
df["Client_Tier"] = pd.cut(
    df["Client_Rating"],
    bins=[0, 3, 4.5, 5],
    labels=["Low", "Mid", "High"]
)

# Схема и пропуски
schema = df.dtypes.to_frame("dtype")
schema["missing_values"] = df.isnull().sum()
schema["non_null_count"] = df.notnull().sum()
schema.to_csv("notebooks/schema.csv")

# Уникальные значения по ключевым полям
categorical_cols = ["Payment_Method", "Client_Region", "Experience_Level", "Region_Short", "Hourly_Band", "Job_Range_Label", "Client_Tier"]
with open("notebooks/categorical_summary.txt", "w", encoding="utf-8") as f:
    for col in categorical_cols:
        f.write(f"{col}:\n")
        f.write(", ".join(map(str, df[col].unique())) + "\n\n")

# Статистика по числовым
numeric_cols = ["Earnings_USD", "Job_Completed", "Hourly_Rate", "Earnings_per_Project"]
summary = df[numeric_cols].describe()
summary.to_csv("notebooks/numeric_summary.csv")

# Сохраняем очищенные и обогащённые данные
df.to_csv("notebooks/enriched_freelancer_data.csv", index=False)
