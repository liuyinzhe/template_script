# B站 https://www.bilibili.com/video/av927393080/
# 根据理解修改python版

#动态规划的思想，就是最优解 拆分为最有1步骤 + 前面n-1 步骤的最优解
#从最小的开始开始推演

amount=63 # 目标金额
coins=[1,2,5,7,10] #硬币金额
dp = [-1]*(amount+1) #建立0-amount位置长度的 数组向量
dp[0] = 0 # 金额0的最优解是0个coins
# 金额为1 的最优解  ，拆分为 1金额+ 0金额的最优解dp[0]
# 从[1,2,5,7,10] 中任意一个硬币 + dp[0]
# 只有硬币 1金额的硬币1 可以， 需要的硬币就是1+dp[] = 1 + 0 =1

# 金额为3的 最优解，可用硬币小于等于3 ，【1，2】可以拆分为  硬币1 + dp[2] 或者 硬币2 + dp[1] 可以得到3
# 可以解 为  【硬币1或者硬币2】 + dp[2/1] = 1 + 1 = 2

# 硬币问题,从0开始，迭代，找最优解，最
for i in range(amount+1): # 目标的最优解，拆分为0-amount 的每一个的最优解
    #
    for j in range(len(coins)):#循环所有硬币，指定1 个硬币金额 coins[j]，作为解 dp[i-coins[j]]+1
        #硬币金额效于目标，并且，减去硬币金额后的 金额数在 dp 数组向量中有最优解存储
        if coins[j]<=i and dp[i-coins[j]]!=-1:
            
            #假设 dp[i-coins[j]] + 1枚硬币
            if dp[i]==-1 or dp[i]>dp[i-coins[j]]+1:
                        dp[i]=dp[i-coins[j]]+1
    print(dp)
    print(len(dp))
    print(dp[amount])
