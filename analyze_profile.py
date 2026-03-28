import pstats

# 读取性能分析结果
p = pstats.Stats('profile.out')

# 按照累计时间排序并显示前20个函数
print("\n=== 按累计时间排序的前20个函数 ===")
p.sort_stats('cumulative').print_stats(20)

# 按照执行时间排序并显示前20个函数
print("\n=== 按执行时间排序的前20个函数 ===")
p.sort_stats('time').print_stats(20)
