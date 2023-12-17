def lengthOfLongestSubstring(s:str):
    s = [c for c in s]
    lgst = []
    len_list = []
    index = 0
    for c in s:
        if c not in lgst:  #当没有在暂存块中就加入c
            index += index
            lgst.append(c)
            len_list.append(len(lgst))
            print(lgst)
        elif c in lgst:
            #如果发现暂存库中有c那么开始截断暂存块，并计算暂存块长度
            len_list.append(len(lgst))
            #开始初始化暂存快,并记录重复元素的位置，继续滑动。

            index += index
            r_index = 0  #lgst暂存快中a的下标
            for r in lgst:

                if r == c:

                    print('r='+r)
                    print('c='+c)
                    lgst = lgst[r_index+1:]
                    lgst.append(c)
                    print(r_index)
                    # lgst.append(c)
                    print(str(lgst)+'每段')
                r_index = r_index + 1
                # if c == s[index+1]:


            #012345679
            #opacdbfaegh


    max = 0
    for num in len_list:
        if num > max:
            max = num
        elif num < max:
            max = max
        elif num == max:
            max = num
    print(max, len_list)
    return max

lengthOfLongestSubstring('dvdf')