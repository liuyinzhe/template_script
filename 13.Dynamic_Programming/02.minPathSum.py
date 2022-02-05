
# b站 https://www.bilibili.com/video/BV15y4y1J7xt


# 思想，最后一步的路线分支中的最优解 + 最后一个位置的总长度

# 计算简单的 0行n列的最优解，累加
# 计算简单的 0列n行的最优解，累加

# 最终路径二叉选择 + 最终的值的长度

import numpy as np

#grid  为二维数组

def minPathSum(grid):
    grid = np.array(grid)
    print("grid")
    print(grid)
    print("\n")
    r,c = grid.shape
    # 建立一个相同shape的多为数组dp 存储每个位置的最短距离之和
    dp = np.array([[0]*c]*r)
    
    dp[0][0] = grid[0][0];

    # 第一列的所有值累加，计算每个位置直线最短距离
    for i in range(1,r):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    
    # 第一行的所有值累加，计算每个位置直线最短距离
    for j in range(1,c):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    
    # 两边的最短距离有了，[0,0]位置也有了，开始计算对角线上的
    # min([1,0]位置最短距离,[0,1]位置最短距离) + [1,1] 位置的数值 = 到[1,1]距离的最短距离
    for i in range(1,r):
        for j in range(1,c):
            dp[i][j] = min(dp[i-1][j],dp[i][j-1])+grid[i][j]
    print("dp")
    print(dp)
    return dp[r-1][c-1]


grid = [
    [1,3,1],
    [1,5,1],
    [4,2,1],
]

print('minPathSum:',minPathSum(grid))

# dp = [
#     [1,4,5],
#     [2,7,6],
#     [6,8,7],
# ]


# b=np.array(grid)
# print(b.shape)
# r,c=b.shape
# x= np.array([[0]*c]*r)
# print(x.shape)


