# pttcrawer
## 基本說明
 - 可以對台灣知名的bbs站ptt上的文章進行簡單的分析

## 主要功能
 - 取得文章資訊
 - 取得推文資訊

## example
 - 見example.py，直接執行可得針[這篇文章](https://www.ptt.cc/bbs/Gossiping/M.1453350815.A.725.html)的時間對推文累積量的作圖，由此可以觀察到推文隨著時間過去會有飽和的現象
![image](https://github.com/ap9035/pttcrawer/blob/master/fig1.png)
 - example.py : example5 表特下載功能，設定開始頁面、結束頁面以及標準，可以下載該範圍內推文的表特圖
![image](https://github.com/ap9035/pttcrawer/blob/master/fig2.png)
![image](https://github.com/ap9035/pttcrawer/blob/master/fig3.png)

## 參考：
 - PTT 評論行為分析 – 以太陽花學運期間為例/ 王銘宏(http://whogovernstw.org/2016/01/05/minghungwang1/)
 - 部分程式碼修改自：https://github.com/JIElite/PTT_Beauty_Spider

## TODO
 - 備份文章的功能(使用sqlite)
 - XX之亂的預測
 - 圖形介面？
