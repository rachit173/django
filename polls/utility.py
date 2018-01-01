def con(ans,section):
    # if section not in [1,2,3]: return None
    num=[]
    if section==1:
        ans = ans.lower()
        num = []
        if 'a' in ans: num.append('a')
        elif 'b' in ans: num.append('b')
        elif 'c' in ans: num.append('c')
        elif 'd' in ans: num.append('d')
        return sorted(num)
    elif section==2:
        num = []
        if 'a' in ans: num.append('a')
        if 'b' in ans: num.append('b')
        if 'c' in ans: num.append('c')
        if 'd' in ans: num.append('d')
        return sorted(num)
    elif section==3:
        num = []
        try:
            num.append(int(ans))
        except:
            pass
        return sorted(num)
    else:
        return None    

def decon(num,section):
    if section==1:
        ret = []
        for i in range(4):
            if num%2==1:
                ret.append(chr(ord('a')+i))
                return ret
            num/=2
    elif section==2:
        ret = []
        for i in range(4):
            if num%2==1:
                ret.append(chr(ord('a')+i))
            num/=2
        return sorted(ret)
    elif section==3:
        ret = [num]
        return sorted(ret)
    else:
        return None

def calc(res,ans,tot,neg,par,section):
    if res==None: return 0
    if ans==None: 
        print "Bonus"
        return tot
    try:
        tot = int(tot)
    except:
        tot = 0
    try:
        neg = -1*abs(int(neg))
    except:
        neg = 0
    try:
        par = int(par)
    except:
        par = 0
    if section==1:
        if res[0]==ans[0]: return tot
        else: return neg
    elif section==2:
        ret=0
        if res==ans: return tot
        else:
            for e in res:
                if e not in ans: return neg
                else: ret+=par
            return ret
    elif section==3:
        if res[0]==ans[0]: return tot
        else: return neg
    print "Reached the end of conditional execution in\
            calc() method,hence return 0"
    return 0