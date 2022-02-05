# B站 https://www.bilibili.com/video/av927393080/


//dp 

using namespace std;
class Solution{
public:
    int coinChange(vector<int>&coins,int amount){
        //初始化数组dp,大小为 amount+1； # indx 作为求解数值，内容为最优解结果
        vector<int>dp(amount + 1 , -1);//全部数值初始化为-1，作为没有计算最优解的标记
        dp[0]=0  //初始化，0的最优解就是0
        //计算金额1至amount的最优解
        for(int i = 1;i<=amount;i++){ 
            //根据硬币类型总数，0开始index
            for(int j=0;j<coins.size();j++){
                // coins[j] 金额 小于 目标数值i ,并且，dp最优解中 1-当前金额的数值 在dp 中有存储最优解答案
                if(coins[j]<=i && dp[i-coins[j]]!=-1){
                    
                    if(dp[i]==-1|| dp[i]>dp[i-coins[j]]+1){
                        dp[i]=dp[i-coins[j]]+1;//更新dp[i]
                }
                }
            }
        }
        return dp[amount];
    }
};


int main(){
    vector<int>coins;//设置面值大小为(1,2,5,7,10)
    coins.push_back(1)
    coins.push_back(2)
    coins.push_back(5)
    coins.push_back(7)
    coins.push_back(10)
    Solution solution;
    printf("%d\n",solution.coinChange(coins,14))
    return 0;
}
