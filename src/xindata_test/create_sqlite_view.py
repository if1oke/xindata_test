import sqlite3


def create_views(db_path="freelancers.db") -> None:
    """
    Создает представления в БД

    param: db_path: файл базы данных
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    views = [
        # Основной summary
        """
        CREATE VIEW IF NOT EXISTS freelancer_summary AS
        SELECT
            Region_Short,
            Is_Expert,
            Hourly_Band,
            Job_Range_Label,
            Client_Tier,
            COUNT(*) AS Count,
            ROUND(AVG(Earnings_USD), 2) AS Avg_Earnings,
            ROUND(AVG(Hourly_Rate), 2) AS Avg_Hourly,
            ROUND(AVG(Rehire_Rate), 2) AS Avg_Rehire
        FROM freelancers
        GROUP BY
            Region_Short, Is_Expert, Hourly_Band, Job_Range_Label, Client_Tier;
        """,
        # По опыту
        """
        CREATE VIEW IF NOT EXISTS project_distribution_by_experience AS
        SELECT
            Experience_Level,
            Job_Range_Label,
            COUNT(*) AS Freelancer_Count,
            ROUND(AVG(Job_Completed), 1) AS Avg_Projects,
            ROUND(SUM(Earnings_USD), 2) AS Total_Earnings
        FROM freelancers
        GROUP BY Experience_Level, Job_Range_Label;
        """,
        # Клиенты
        """
        CREATE VIEW IF NOT EXISTS client_rating_stats AS
        SELECT
            Client_Region,
            Client_Tier,
            COUNT(*) AS Freelancer_Count,
            ROUND(AVG(Client_Rating), 2) AS Avg_Rating,
            ROUND(AVG(Rehire_Rate), 2) AS Avg_Rehire,
            ROUND(SUM(Earnings_USD), 2) AS Total_Earnings
        FROM freelancers
        GROUP BY Client_Region, Client_Tier;
        """,
        # High earners
        """
        CREATE VIEW IF NOT EXISTS high_earner_summary AS
        SELECT
            Region_Short,
            Hourly_Band,
            COUNT(*) AS High_Earner_Count,
            ROUND(AVG(Earnings_USD), 2) AS Avg_Earnings,
            ROUND(AVG(Job_Completed), 1) AS Avg_Jobs
        FROM freelancers
        WHERE High_Earner = 1
        GROUP BY Region_Short, Hourly_Band;
        """,
    ]

    for v in views:
        cursor.execute(v)

    conn.commit()
    conn.close()

    print("View созданы.")


if __name__ == "__main__":
    create_views()
