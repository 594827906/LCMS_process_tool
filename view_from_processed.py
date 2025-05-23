import pandas as pd
import gc


def tic_from_csv(file, label, mode):  # 从处理后的csv中绘制TIC图
    time = []
    tic = []
    df = pd.read_csv(file)
    df = df.sort_values(['scan', 'mz'])  # 按指定列排序
    max_scan = df.iloc[-1]['scan']  # 获取最大scan数
    min_scan = df.iloc[0]['scan']  # 获取最小scan
    max_time = df.iloc[-1]['RT']  # 获取最小time
    scan_freq = max_time / min_scan  # 对扫描频率的估算，非常不准
    max_scan = max_scan.astype(int)  # 转换为整型
    time.append(0)
    tic.append(0)
    for scan in range(1, max_scan):
        if (df['scan'] == scan).any():
            tot_intensity = df.loc[df['scan'] == scan, 'intensity'].sum()  # get total ion of scan
            tic.append(tot_intensity)
            t = df.loc[df['scan'] == scan, 'RT'].values[0]  # get scan time
            time.append(t)
        else:
            if (df['scan'] == scan-1).any():
                t = df.loc[df['scan'] == scan - 1, 'RT'].values[0]
                time.append(t)
                tic.append(0)
            if (df['scan'] == scan+1).any():
                t = df.loc[df['scan'] == scan + 1, 'RT'].values[0]
                time.append(t)
                tic.append(0)

    del df
    gc.collect()  # 回收内存
    return {'x': time, 'y': tic, 'label': label, 'mode': mode}

# obj = construct_df(path)
#
# x = obj['x']
# y = obj['y']
# label = obj['label']

# fig = plt.figure()
# plt = fig.add_subplot(111)
# plt.set_title('Sample')
# plt.legend(loc='best')
# plt.grid(alpha=0.8)
# plt.plot(x, y, label=label)
# plt.show()
