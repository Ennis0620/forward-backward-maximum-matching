import re
import matplotlib.pyplot as plt
import time





def draw_most_word(word,fre,b): 
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta'] #用來正常顯示中文標籤
    
    parameters = {'xtick.labelsize': 25,'ytick.labelsize': 35}#修改坐標軸的文字大小
    plt.rcParams.update(parameters)
    
    plt.figure(figsize=(60, 40))
    plt.style.use("ggplot")
    
    plt.xticks(rotation=90)
      
    plt.plot(word,fre)
    
    plt.title("單字出現頻率表", fontsize = 50)
    plt.xlabel("字詞", fontsize = 40)
    plt.ylabel("出現頻率", fontsize = 40)
    
    plt.savefig(b+"_test_word_fre.png")

#正向分割
def forward_seg(source_sentence,word_dic,max_word_length):
    
    #在dic中找到 切分的字串 
    seg_string=[]   
    sum_len=0   
    original = source_sentence    
    
    while(len(source_sentence)>0):               
        #如果不再字典中
        if(source_sentence not in word_dic):
            #找字典中最長的字，所以不用每次都要整句開始找 只要從最長字的數字開始縮小就好           
            #如果字串長度>字典中最長的字 那麼要從字典中最長的字數開始切 
            if(len(source_sentence)>max_word_length):               
                source_sentence = source_sentence[:max_word_length]
            #否則就一個一個慢慢切    
            else:
                #
                source_sentence = source_sentence[:len(source_sentence)-1] 
        else:
            #統計目前分割完的字總共多長
            sum_len+=len(source_sentence)
            #加入串列中
            seg_string.append(source_sentence)
            #字典出現次數+1
            word_dic[source_sentence]+=1
            #source_sentence 就 變成原本完整句子的字串 扣除 前面分割完的字句
            source_sentence =  original[sum_len:]
            
    #print(seg_string)
    return seg_string   
        

#反向分割
def backward_seg(source_sentence,word_dic_back,max_word_length):
    #在dic中找到 切分的字串 
    seg_string=[]
    
    sum_len=0
    
    original = source_sentence    
    
    while(len(source_sentence)>0):
                
        #如果不再字典中
        if(source_sentence not in word_dic_back):
            #從字典中最長的字，所以不用每次都要整句開始找 只要從最長的字數字開始縮小就好
            
            #如果字串長度>=字典中最長的字 那麼要從字典中最長的字數開始切 
            if(len(source_sentence)>max_word_length):
                
                source_sentence = source_sentence[len(source_sentence)-max_word_length:len(source_sentence)+1]
                

                
            #否則就一個一個慢慢切    
            else:
                #
                source_sentence = source_sentence[1:] 
                
        else:
            
            #統計目前分割完的字總共多長
            sum_len+=len(source_sentence)
            #加入串列中
            seg_string.append(source_sentence)
            #字典出現次數+1
            word_dic_back[source_sentence]+=1
            #source_sentence 就 變成原本完整句子的字串 扣除 前面分割完的字句
            source_sentence =  original[:len(original)-sum_len]
            
            
        
    
    #print(seg_string[::-1])
    return seg_string[::-1] 
           

#計算分詞後與正確答案重合的部分
def same_forward_slice(forward_slice,per_sentence,source_sentence):
    
    correct_set=[]
    forward_set=[]   
    #先將答案的空白split=>找出正確斷句
    per_sentence = per_sentence.strip("\n").split(" ") 
    #迴圈取得正確答案在整段文字的index在哪裡
    i = 0
    for index,per in enumerate(per_sentence):
        #利用分割的長度 [項目,的,研究] 找到各自的index所在範圍      
        correct_set.append( str(i)+","+ str((i+len(per)-1)))
        #print(i,i+len(per)-1)
        #print(source_sentence[i:i+len(per)])
        i+=len(per) 
    #迴圈取得正向分割在整段文字的index在哪裡
    j = 0  
    for index,per in enumerate(forward_slice):
        #利用分割的長度 [項目,的,研究] 找到各自的index所在範圍
        #將分割的index放到set中，方面計算分割相同的有哪些
        forward_set.append( str(j)+","+ str((j+len(per)-1)))     
        #print(j,j+len(per)-1)
        #print(source_sentence[j:j+len(per)])
        j+=len(per)
    #計算分割正確的數量
    score = set(forward_set) & set(correct_set)
    
    return len(score)

def same_backward_slice(backward_slice,per_sentence,source_sentence):
    
    correct_set=[]
    backward_set=[]
    
    #先將答案的空白split=>找出正確斷句
    per_sentence = per_sentence.strip("\n").split(" ")
    
    
    #迴圈取得正確答案在整段文字的index在哪裡
    i = 0
    for index,per in enumerate(per_sentence):
        #利用分割的長度 [項目,的,研究] 找到各自的index所在範圍
        
        correct_set.append( str(i)+","+ str((i+len(per)-1)))
        #print(i,i+len(per)-1)
        #print(source_sentence[i:i+len(per)])
        i+=len(per)
    
    #迴圈取得反向分割在整段文字的index在哪裡
    j = 0
    
    for index,per in enumerate(backward_slice):
        #利用分割的長度 [項目,的,研究] 找到各自的index所在範圍
        #將分割的index放到set中，方面計算分割相同的有哪些
        backward_set.append( str(j)+","+ str((j+len(per)-1)))
        
        #print(j,j+len(per)-1)
        #print(source_sentence[j:j+len(per)])
        j+=len(per)
    
    
    #計算分割正確的數量
    score_backward = set(backward_set) & set(correct_set)
    
    return len(score_backward)


count = 0 #計算目前處理資料的筆數
word_dic = {} #建立常用字詞的字典
max_word_length = 0 #常用字典中最長句子的長度


correct_slice_num = 0
forward_slice_num = 0   
backward_slice_num = 0
#和正確答案分割相同的組數
score=0
score_backward = 0                    

start = time.time()

#30萬單字數量
with open("lexicon1_raw_nosil.txt",encoding='utf-8-sig') as fp:
    per_line = fp.readlines()
    for dic in per_line:
        dic_split = dic.split(" ")
        word_dic.setdefault(dic_split[0],0)       
        #找出常用字典中最長的字 以每次切分時從此長度進行判斷
        if max_word_length<len(dic_split[0]):            
            max_word_length = len(dic_split[0])
         
        

#反向分割的字典
word_dic_back= word_dic.copy()
        

#要切分的3G檔案    
with open("GigaWord_text_lm.txt",encoding='utf-8-sig') as fp:
    per_line = fp.readlines()
    for per_sentence in per_line:
        
        count+=1
        
        #先去掉空白(因為原先的是準答案) r'[^\u4e00-\u9fa5]'為去掉所有非中文
        source_sentence = re.sub(r'[^\u4e00-\u9fa5]', "",per_sentence) 
        #正向匹配
        forward_slice = forward_seg(source_sentence,word_dic,max_word_length)
        #反向匹配
        backward_slice = backward_seg(source_sentence,word_dic_back,max_word_length)               
        #表準答案總共分割幾組
        correct_slice_num += len(per_sentence.split(" "))      
        #正向匹配總共分割幾組
        forward_slice_num += len(forward_slice)
        #反向匹配總共分割幾組
        backward_slice_num += len(backward_slice)
        
        #計算正向分割後和正確答案分詞重合的 次數
        score += same_forward_slice(forward_slice,per_sentence,source_sentence)
        #計算反向分割後和正確答案分詞重合的 次數
        score_backward += same_backward_slice(backward_slice,per_sentence,source_sentence)            
        
        if count%50000==0:
            print("目前資料處理數量:",count,"筆")


precision_forward = (score/forward_slice_num)*100
recall_forward = (score/correct_slice_num)*100
print("------正向最長匹配--------")
print("score:",score)
print("correct_slice_num:",correct_slice_num)
print("forward_slice_num:",forward_slice_num)
print("精準度:",score,"/",forward_slice_num,"=",precision_forward,"%")
print("召回率:",score,"/",correct_slice_num,"=",recall_forward,"%")
print("F1:", (2*precision_forward*recall_forward)/(precision_forward+recall_forward))


precision_backward = (score_backward/backward_slice_num)*100
recall_backward = (score_backward/correct_slice_num)*100
print("------反向最長匹配--------")
print("score_backward:",score_backward)
print("correct_slice_num:",correct_slice_num)
print("backward_slice_num:",backward_slice_num)
print("精準度:",score_backward,"/",backward_slice_num,"=",precision_backward,"%")
print("召回率:",score_backward,"/",correct_slice_num,"=",recall_backward,"%")
print("F1:", (2*precision_backward*recall_backward)/(precision_backward+recall_backward))


#正向分割排序       
dic_sort = sorted(word_dic.items(),key=lambda item:item[1],reverse=True)

#反向分割排序
dic_back_sort = sorted(word_dic_back.items(),key=lambda item:item[1],reverse=True)

end = time.time()
print("-------------------")
print ("秒數:", round((end-start),5))
print("分鐘數:", round((end-start)/60,5))
print("小時數:", round((end-start)/60/60,5))

'''
#畫圖X，Y軸        
list_forward_x = []
list_forward_y = []
list_backward_x = []
list_backward_y = []            


for index,i in enumerate(dic_sort): 
    if index < 100:    
        list_forward_x.append(i[0])
        list_forward_y.append(i[1])
    else:
        break

draw_most_word(list_forward_x,list_forward_y,"forward_")


for index,i in enumerate(dic_back_sort):    
    if index < 100:
        list_backward_x.append(i[0])
        list_backward_y.append(i[1])
    else:
        break
    
draw_most_word(list_backward_x,list_backward_y,"backward_")

'''


