巨量資料-正向、反向最長匹配之結果
===

SIC-XE 
# Introduction
使用前向長詞優先和後向長詞優先演算法對巨量資料進行斷詞處理，並統計跟正確斷詞答案的Recall、accuracy、F1。

# Detail
### 讀檔:
1.讀取30萬常用字辭典，並在讀取時紀錄最長字數(優化關鍵)。

2.將巨量資料(內容是已經分割過的標準答案)的分割空白消除。
### 正向:
1.從整段文字開始往前搜尋

    ex:項目的研究

2.不在常用字辭典內就減少1個字，看是否在辭典中 

    ex: 項目的研、項目的、項目
    
3.找到出現在辭典內之詞進行分割 
    
    ex.項目,的研究

4.繼續2的步驟直到被分割完 

    ex.項目,的,研究
    
### 反向:

1.從整段文字開始往後搜尋

    ex.項目的研究

2.不在常用字辭典內就減少1個字，看是否在辭典中

    ex. 目的研究、的研究、研究
    
3.找到出現在辭典內之詞進行分割 

    ex.項目的,研究
    

4.繼續2的步驟直到被分割完 

    ex.項目,的,研究
    
### 計算Recall、accuracy、F1:
將(正確答案&正反向)分割後的結果給予index,index的標記 

    ex. 正確:項(0)目(1),的(2),研(3)究(4) => (0,1)(2,2)(3,4)
	    正向:項(0)目(1),的(2),研(3)究(4) => (0,1)(2,2)(3,4)
	    反向:項(0),目(1)的(2),研(3)究(4) => (0,0)(1,2)(3,4)

使用set去計算重合部分
    
    ex. 正向: P=3/3=100% R=3/3=100% F1=(2*100%*100%)/(100%+100%)=100%
        反向: P=1/3=33% R=1/3=33% F1=(2*33%*33%)/(33%+33%)=33%


# Demo

示意圖

![](https://i.imgur.com/AOJqs2Z.png)

優化前結果

![](https://i.imgur.com/lTa9yCY.png)

優化後結果

![](https://i.imgur.com/BruJcsY.png)

# Requirement
    matplotlib
    re
# Package
    ─forward-backward-seg
        backward__test_word_fre.png      後向分割出現前100名
        forward__test_word_fre.png       前向分割出現前100名
        lexicon1_raw_nosil.txt           常用字辭典
        NLP_Forward_and_backward.py      主程式
        優化前.PNG                        優化前時間
        優化後.PNG                        優化後時間

# Problems
1.如何加快匹配速度

# Solve
1.紀錄常用自辭典內字數最長的
2.thread 可是python thread還是會鎖住 較適合用來做爬蟲類的I/O