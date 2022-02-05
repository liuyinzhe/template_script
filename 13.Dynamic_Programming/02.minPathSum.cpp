
// b站 https://www.bilibili.com/video/BV15y4y1J7xt

using namespace std;
class Solution{
public:
    int minPathSum(vector<vector<int> >& grid){ //二维数组向量 命名为grid
        int r = grid.size(); //数组的行
        int c = grid[0].size(); //数组的列
        vector<vector<int> > dp(r,vector<int>(c,0)); //存储每个位置的最优解
        
        dp[0][0] = grid[0][0]; //0-0位置的最优解等于该位置的值
        for (int i = 1; i < c; i++){ //循环i，计算第i列的最优解
            dp[0][i] = dp[0][i-1] + grid[0][i]; //等于第一列的最优解加上该列的值
        }
        for  (int i = 1; i < r; i++){  //循环i, 计算第i行的最优解
            dp[i][0] = dp[i-1][0] + grid[i][0]; //等于前一行的最优解加上该行的值
        }
        //从第一行到r-1行，从第一列到c-1列，计算每个位置的最小路径之和
        for (int i= 1; i < r; i++){
            for (int j = 1; j < c; j++){
                //位置(i,j)的最优解，等于上方位置和左侧位置中较小的，加上该位置的值
                dp[i][j] = min(dp[i-1][j],dp[i][j-1])+grid[i][j]

            }
        }
        return dp[r-1][c-1]; //返回右下角最优解
    }
};
