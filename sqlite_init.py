import sqlite3
import csv
import os

def init_database():
    """初始化 SQLite 数据库并导入 telco 数据"""
    
    # 数据库文件路径
    db_path = 'telco.db'
    csv_path = 'telco_data.csv'
    
    # 如果数据库已存在，删除它以重新创建
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"已删除旧的数据库文件: {db_path}")
    
    # 连接到 SQLite 数据库（如果不存在会自动创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"成功创建数据库: {db_path}")
    
    # 创建 telco 表
    create_table_sql = """
    CREATE TABLE telco (
        customerID TEXT PRIMARY KEY,
        gender TEXT,
        SeniorCitizen INTEGER,
        Partner TEXT,
        Dependents TEXT,
        tenure INTEGER,
        PhoneService TEXT,
        MultipleLines TEXT,
        InternetService TEXT,
        OnlineSecurity TEXT,
        OnlineBackup TEXT,
        DeviceProtection TEXT,
        TechSupport TEXT,
        StreamingTV TEXT,
        StreamingMovies TEXT,
        Contract TEXT,
        PaperlessBilling TEXT,
        PaymentMethod TEXT,
        MonthlyCharges REAL,
        TotalCharges TEXT,
        Churn TEXT
    )
    """
    
    cursor.execute(create_table_sql)
    print("成功创建表: telco")
    
    # 读取 CSV 文件并插入数据
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        insert_sql = """
        INSERT INTO telco (
            customerID, gender, SeniorCitizen, Partner, Dependents, tenure,
            PhoneService, MultipleLines, InternetService, OnlineSecurity,
            OnlineBackup, DeviceProtection, TechSupport, StreamingTV,
            StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
            MonthlyCharges, TotalCharges, Churn
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        row_count = 0
        for row in csv_reader:
            cursor.execute(insert_sql, (
                row['customerID'],
                row['gender'],
                int(row['SeniorCitizen']),
                row['Partner'],
                row['Dependents'],
                int(row['tenure']),
                row['PhoneService'],
                row['MultipleLines'],
                row['InternetService'],
                row['OnlineSecurity'],
                row['OnlineBackup'],
                row['DeviceProtection'],
                row['TechSupport'],
                row['StreamingTV'],
                row['StreamingMovies'],
                row['Contract'],
                row['PaperlessBilling'],
                row['PaymentMethod'],
                float(row['MonthlyCharges']),
                row['TotalCharges'],
                row['Churn']
            ))
            row_count += 1
        
        conn.commit()
        print(f"成功插入 {row_count} 条数据到 telco 表")
    
    # 查询并打印前 5 行数据
    print("\n" + "="*100)
    print("查询结果 - 前 5 行数据:")
    print("="*100)
    
    cursor.execute("SELECT * FROM telco LIMIT 5")
    rows = cursor.fetchall()
    
    # 获取列名
    column_names = [description[0] for description in cursor.description]
    
    # 打印列名
    print("\n{:<15} {:<8} {:<6} {:<8} {:<12} {:<7} {:<13} {:<20} {:<15}".format(
        'customerID', 'gender', 'Senior', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'Internet'
    ))
    print("-" * 100)
    
    # 打印数据行
    for row in rows:
        print("{:<15} {:<8} {:<6} {:<8} {:<12} {:<7} {:<13} {:<20} {:<15}".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
        ))
    
    print("\n" + "="*100)
    
    # 查询总记录数
    cursor.execute("SELECT COUNT(*) FROM telco")
    total_count = cursor.fetchone()[0]
    print(f"数据库中总记录数: {total_count}")
    print("="*100)
    
    # 关闭连接
    conn.close()
    print("\n数据库初始化完成！")

if __name__ == "__main__":
    init_database()

