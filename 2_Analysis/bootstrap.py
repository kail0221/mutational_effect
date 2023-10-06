import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from openpyxl import Workbook
from multiprocessing import Pool, cpu_count

def calculate_bootstrap(num_values):
    df = pd.read_excel('./sample.xlsx')
    ColNames_List = df.columns.values.tolist()
    sample_mean_dict = {}
    pearson_dict = {}

    for col in ColNames_List:
        sample_mean_list = []

        for i in range(100000):
            index = np.random.choice(range(6), num_values)
            sample_mean_list.append(np.mean(df[col][index]))

        sample_mean_dict[col] = sample_mean_list

    # 将字典转换为 DataFrame
    result_df = pd.DataFrame(sample_mean_dict)
    exp ={'wt':-9.283159731,
       '2l':-11.63810099,
       '2m':-10.59270558,
       '2i':-10.15249428,
       '1f':-9.896812903,
       '1w':-8.432598383,
       '1y':-9.69627545,
       '3w':-10.24238473,
       '3f':-9.852644552,
       '3y':-10.26576027,
       '3a':-9.633480583,
       '3m':-10.15249428,
       '3s':-8.502797072,
       '2l3w':	-12.03964353,
       '2l3f':	-11.93795072,
       '2l3y':	-11.40214718,
       '2l3a':	-10.89715765,
       '2l3m':	-11.15191428,
       '2l3s':	-10.56561,
       '1w2l':	-10.89715765,
       '1f2l':	-11.88735065,
       '1y2l':	-11.8642768}
    result_df.loc[len(result_df.index)] = exp

    # 计算每一行与最后一行的 Pearson 相关系数
    result_df['Pearson Correlation'] = result_df.iloc[:-1].apply(lambda row: pearsonr(row, result_df.iloc[-1])[0], axis=1)
    result_mean = result_df['Pearson Correlation'].mean(axis=0)    
    result_std = result_df['Pearson Correlation'].std(axis=0,ddof=0)
    result_df.loc['平均值',['Pearson Correlation']]=result_mean
    result_df.loc['标准差',['Pearson Correlation']]=result_std
    
    # 获取取值数量作为 sheet 名称
    sheet_name = str(num_values)
    
    #将pearson结果写入一个excel表中
    pearson_dict[sheet_name] = []
    pearson_dict[sheet_name].append(result_mean)
    pearson_dict[sheet_name].append(result_std)
    print(pearson_dict)
    # 返回结果
    return (sheet_name, result_df)

if __name__ == '__main__':
    # 获取CPU核心数
    num_cores = 6

    # 创建 ExcelWriter 对象
    excel_file = './localhome/zmc/1tvb/summary/math_result/dVDW_IE_bootstrap-asie1-mhc.xlsx'
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # 创建进程池
    pool = Pool(processes=num_cores)

    # 遍历取值数量
    num_values_list = range(1, 7)

    # 并行计算
    results = pool.map(calculate_bootstrap, num_values_list)

    # 关闭进程池
    pool.close()
    pool.join()

    # 将结果写入 Excel 文件
    for sheet_name, result_df in results:
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # 保存 Excel 文件
    writer.save()
