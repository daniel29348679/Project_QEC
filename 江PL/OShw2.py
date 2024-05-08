import queue

class Process:
    def __init__(self, process_id, cpu_burst, arrival_time, priority):
        self.process_id = process_id
        self.cpu_burst = cpu_burst
        self.arrival_time = arrival_time
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
    
class Element:
    def __init__(self, pri1, pri2, pro):
        self.pri1 = pri1
        self.pri2 = pri2
        self.pro =  pro

    def __lt__(self, other):
        if self.pri1 == other.pri1:
            return self.pri2 < other.pri2
        return self.pri1 < other.pri1
    
    def get_info(self):
        return self.pri1, self.pri2, self.pro

        

filename = input("Please enter a file name: ")

def Gantt_id(process_id):
    if process_id <= 9 and process_id >= 0 :
        return str(process_id)
    else :
        return chr(55+process_id)

processes = []
# 0<=process編號<=36
with open(filename, 'r') as file:
    first_line = file.readline().strip()
    method, time_slice = first_line.split()
    method = int(method)
    time_slice = int(time_slice)
    second_line = file.readline().strip()
    strings = second_line.split()
    for line in file:
        line = line.strip()
        if not line:
            break
        numbers = map(int, line.split())
        process_id, cpu_burst, arrival_time, priority = numbers
        process = Process(process_id, cpu_burst, arrival_time, priority)
        processes.append(process)

WT = {}  # waiting time
TA = {}  # turnaround time
FT = {}  # finish time
Gantts = [] 
# 以上可先用已知ID全部初始化為6個-1，後續一次只修正一格：WT[0][method-1] = 算出來的waiting time
for p in processes:
    WT[p.process_id] = [-1,-1,-1,-1,-1,-1]
    TA[p.process_id] = [-1,-1,-1,-1,-1,-1]
    FT[p.process_id] = [-1,-1,-1,-1,-1,-1]
meth = ["FCFS", "RR", "SJF", "SRTF","HRRN","PPRR"]

sorted_WT = dict(sorted(WT.items()))
WT = sorted_WT
sorted_TA = dict(sorted(TA.items()))
TA = sorted_TA


def waiting_time(process, mth):
    return FT[process.process_id][mth-1] - process.arrival_time - process.cpu_burst


def Turn_time(process, mth):
    return FT[process.process_id][mth-1] - process.arrival_time

def SJF_cmp(process):
    return (process.cpu_burst, process.arrival_time, process.process_id)

def STRF_cmp(p):
    return (p.cpu_burst, p.arrival_time, p.process_id)

def HRRN_cmp(p):
    return (p.arrival_time, p.process_id)


def schedule(m):
    total = 1
    for p in processes:
        total += p.cpu_burst
    # 畫Gantt_chart直到len(Gantt_chart) == CPU_burst的總和(total)
    # 一邊畫甘特、一邊填FT
    # 照i-learning上下載不了的那個東東寫
    Gantt = ""

    if m == 1: # FCFS
        # 沒有queue，直接遍歷processes找因為條件只有一個就是arrival time而且拿走就不放回
        wait = 0
        cur_time = 0
        cur_p = Process(99, -1, -1, -1)
        done = []
        while cur_time < total:
            # 遍歷找到這秒要做的process 到達了且沒有人跟他等待時間相同
            wait = 0
            for p in processes:
                if (cur_time - p.arrival_time > wait or (cur_time - p.arrival_time == wait and cur_p.process_id > p.process_id)) and p.process_id not in done:
                    cur_p = p
                    wait = cur_time - p.arrival_time
            if cur_p.process_id == 99 :
                Gantt += "-"
                cur_time += 1
            else :
                Gantt += Gantt_id(cur_p.process_id)*cur_p.cpu_burst
                cur_time += cur_p.cpu_burst
                FT[cur_p.process_id][0] = cur_time
                done.append(cur_p.process_id)
            cur_p = Process(99, -1, -1, -1)
        Gantts.append(Gantt)

    elif m == 2: # RR  
        # 進queue之前先排序(重點在進queue的順序)，從get直接拿，拿了還會放回
        # q裡面的cpu_burst是複製出來的
        cur_time = 0
        q = queue.Queue()
        backtoqueue = queue.Queue()
        while cur_time < total:
            # 先加到達的依照id小至大
            newarrive = []
            for p in processes:
                if p.arrival_time == cur_time:
                    newarrive.append(p.process_id)
            temp = sorted(newarrive)
            newarrive = temp
            for n in newarrive:
                for p in processes:
                   if p.process_id == n:
                        q.put(Process(p.process_id,p.cpu_burst,p.arrival_time,p.priority))
            # 再將上次沒做完的放回q
            if not backtoqueue.empty(): # 上次有沒做完的
                q.put(backtoqueue.get())

            if q.empty() :
                Gantt += "-"
                cur_time += 1
            else:
                cur_p = q.get()
                # print("cur_p.process_id=", cur_p.process_id)

                # 這次做不完
                if cur_p.cpu_burst > time_slice:  
                    Gantt += Gantt_id(cur_p.process_id)*time_slice
                    cur_time += time_slice
                    cur_p.cpu_burst -= time_slice
                    backtoqueue.put(cur_p)
                # 本輪會結束
                else :
                    Gantt += Gantt_id(cur_p.process_id)*cur_p.cpu_burst 
                    cur_time += cur_p.cpu_burst  
                    cur_p.cpu_burst = 0
                    FT[cur_p.process_id][1] = cur_time
        Gantts.append(Gantt)

    elif m == 3: # SJF
        cur_time = 0
        picked = [] # done
        while cur_time < total:
            cur_list = []
            for p in processes:
                if cur_time >= p.arrival_time and p.process_id not in picked: # 已到達、未被挑走
                    cur_list.append(p)
            if len(cur_list) == 0:
                cur_time += 1
                Gantt += "-"
                continue
            sorted_list = sorted(cur_list, key= SJF_cmp)  # 反正是我要的方式排序
            p = sorted_list[0]
            picked.append(p.process_id)
            Gantt += Gantt_id(p.process_id)*p.cpu_burst
            cur_time += p.cpu_burst
            FT[p.process_id][2] = cur_time
            # 應該是每做完一個就要再回去找一次
            sorted_list.clear()
            cur_list.clear()
        Gantts.append(Gantt)


    elif m == 4: # SRTF
        cur_time = 0
        copy = []
        while cur_time < total:
            # 這秒新到達的人加入list
            # print("time=", cur_time)
            for p in processes:
                if cur_time == p.arrival_time :
                    copy.append(Process(p.process_id, p.cpu_burst, p.arrival_time, p.priority))
                    # print(copy[len(copy)-1].process_id)
            # 排序
            copy = sorted(copy, key= STRF_cmp)  ###應該是排序排錯
            
            if len(copy) == 0:
                Gantt += "-"
            else:
                # 取第0個填甘特、扣cpu_burst，做完了就填FT
                Gantt += Gantt_id(copy[0].process_id)
                copy[0].cpu_burst -= 1
                if copy[0].cpu_burst == 0:
                    FT[copy[0].process_id][3] = cur_time+1
                    copy.pop(0)
            cur_time += 1
            # 每秒都要更新、重排，取第零個
            # copy = sorted(copy, key= STRF_cmp)
        Gantts.append(Gantt)

    elif m == 5: # HRRN
        cur_time = 0
        qu = []  # 拿了就做完
        done  = []
        while cur_time < total:
            ratio = -1
            for p in processes:
                if cur_time >= p.arrival_time and p.process_id not in done: # 已到達的人才需要比較(做完的要拿走)
                    # 挑相同ratio的人們放入queue，排序後只取第一個，剩下的下次會再被取一次
                    if (p.cpu_burst + cur_time -p.arrival_time)/p.cpu_burst == ratio:
                        qu.append(p)
                    elif (p.cpu_burst + cur_time -p.arrival_time)/p.cpu_burst > ratio:
                        qu.clear()
                        qu.append(p)
                        ratio = (p.cpu_burst + cur_time -p.arrival_time)/p.cpu_burst
            qu = sorted(qu, key= HRRN_cmp)
            if(len(qu) == 0):
                Gantt += "-"
                cur_time += 1
            else :
                cur_time += qu[0].cpu_burst
                Gantt += Gantt_id(qu[0].process_id)*qu[0].cpu_burst
                FT[qu[0].process_id][4] = cur_time
                done.append(qu[0].process_id)
            qu.clear()
        Gantts.append(Gantt)

    elif m == 6: # PPRR
        copy = []
        for p in processes:
            copy.append(Process(p.process_id, p.cpu_burst, p.arrival_time, p.priority))

        cur_time = 0
        pq = queue.PriorityQueue()   # 存一份copy過來的process們   和 兩個優先級 的element
        pri = 99
        cur_p = Process(-1, -1, -1, 99)
        RR = queue.Queue()
        Preemptive = 0
        t = time_slice
        print(time_slice)
        i = 1

        while cur_time < total:
            print("time=", cur_time, "pri=", pri, "cur_p=", cur_p.process_id)
            Preemptive = 0
            # 最最最一開始加入pq時也要給一個加入的順序
            for p in copy:  # 遍歷收集 這秒 到達的人
                if p.arrival_time == cur_time and p.priority >= pri:  # 新來的 不搶 上個人
                    if p.priority == pri :  # 直接放RR
                        print("+", p.process_id, "to RR")
                        RR.put(p)
                    else : # 廢物 去一邊
                        pq.put(Element(p.priority, i ,p))#################################
                        i += 1
                        print("+", p.process_id, "to pq," , p.priority, i)
                elif p.arrival_time == cur_time and p.priority < pri :# 新來的 搶 上個人
                    Preemptive = 1
                    pq.put(Element(p.priority, i, p))#################################
                    i += 1
                    pri = p.priority
                    print("+", p.process_id, "to pq, expected to renew the pri as", p.priority, i)
 
                    # what if 這秒無人到達所以上個人繼續做 or 這秒有新來的但上個RR全做完 or 這秒無人到達且上個RR全做完


            if pq.empty():  # 尚無人到達
                cur_time += 1
                Gantt += "-" 
                continue
            
            # 不搶
            if Preemptive == 0:# 都檢查完(新加的加到RR)後才可以把上輪time out沒做完所以保留到現在的cur_p放回RR
                if not cur_p.process_id == -1:
                    if t == 0: 
                        print("last one =", cur_p.process_id , "time out, put back")
                        RR.put(cur_p)  
                        cur_p = RR.get()
                        t = time_slice
                    else :
                        print("last one =", cur_p.process_id , "should keep doing")
                else:
                    # 若剛剛RR做完、cur_p被reset成-1，又剛好這秒沒東西到達(或是新來的pri很大被放後面)->Preemptive都會是0，都要重組
                    # 重組RR!
                    print("rebuild RR! because run out of")
                    stop = False
                    pri = 99
                    # RR重組 
                    ele = pq.get()
                    pri, n, temp = ele.get_info()  # n是我自己多給的入pq的順序#################################
                    RR.put(temp)
                    print("pri=", pri)
                    print("take", temp.process_id, "to RR,", pri, n)  #########6, 27
                    while not pq.empty() and not stop:
                        ele = pq.get()
                        temp_p, n , temp = ele.get_info()              
                        if temp_p != pri:
                            stop = True 
                            pq.put(Element(temp_p, n, temp))  # 拿錯了所以放回去 #################################
                        else:
                            RR.put(temp)
                            print("take", temp.process_id, "to RR,",temp_p, n)

                    cur_p = RR.get()
                    t = time_slice  
                    print( "cur_p=", cur_p.process_id, ",t=", t)

            # 搶劫！！
            else :
                # RR 清空回到pq 手上的也要放回去
                print("Preemptive !", "pri=", pri )  
                
                
                while not RR.empty() :               # RR裡的後放回pq
                    temp = RR.get()
                    print("   put", temp.process_id, "back to pq(RRq)")
                    pq.put(Element(temp.priority, i, temp))#################################
                    i += 1
                if cur_p.process_id != -1:           # 手上的先放
                    pq.put(Element(cur_p.priority, i, cur_p))#################################
                    i += 1
                    print(" put", cur_p.process_id, "back to pq(hand)")
                
                # 從pq取新的RR並get給cur_p 
                stop = False
                # RR重組 
                ele = pq.get()
                pri, n , temp = ele.get_info()
                RR.put(temp)
                print("rebuild RR! because preemptive, pri change to", pri, n)
                print("take", temp.process_id, "to RR," , pri , n)
                while not pq.empty() and not stop:
                    ele = pq.get()
                    temp_p, n, temp = ele.get_info()                     #################################
                    if temp_p != pri:
                        stop = True 
                        pq.put(Element(temp_p, n, temp))  # 拿錯了所以放回去#################################
                    else:
                        RR.put(temp)
                        print("take", temp.process_id, "to RR,",temp_p, n)

                cur_p = RR.get()
                t = time_slice  
                print("cur_p=", cur_p.process_id, ",t=", t)

                # input1_method6.txt      

    
            # 做cur_p
            cur_p.cpu_burst -= 1
            Gantt += Gantt_id(cur_p.process_id)
            cur_time += 1
            t -= 1
            print(cur_p.process_id, "still left =",cur_p.cpu_burst, "to do, t=", t)
                
            if cur_p.cpu_burst == 0:  # cur_p沒有交接出去
                print(cur_p.process_id, "finish! finish time=", cur_time)
                # 做finish工作
                FT[cur_p.process_id][5] = cur_time
                t = time_slice
                if not RR.empty():  # RR還有 先拿著 回去檢查新來的
                    cur_p = RR.get()
                else:  # RR做完了 檢查過新來之後 要回pq重找一批RR
                    if not pq.empty():# 讓下次新來的很大的pri搶不了pq的頭，才不會算是prieemptive
                        ele = pq.get()
                        next_pri, n, next = ele.get_info()
                        pri = next_pri
                        pq.put(Element(next_pri, n, next))                        #################################
                        # 不是直接期望隨便一個新來的都搶的了，而是要優於pq的頭的才算搶
                    else :
                        pri = 99
                    cur_p = Process(-1, -1, -1, 99)
        Gantts.append(Gantt)
        print(Gantt)

    else:
        print("your Gantt:", len(Gantt))
        print(Gantt)
        print("It should be",total)
        return -9999

    
    # 填WT字典(under此method)
    # 填TA字典(under此method)
    for p in processes:
        TA[p.process_id][m-1] = Turn_time(p, m)
        WT[p.process_id][m-1] = waiting_time(p, m) # 阿如果method是7就GG

    
if method == 7:
    for i in range(1,7):
        schedule(i)
if method >= 1 and method <= 6:
    schedule(method)

if method >= 1 and method <= 6:
    outputfile = "out_" + f"{filename[:6]}" + "_method" + f"{method}" + ".txt"
    with open(outputfile, "w") as file:
        # 甘特圖
        # ID >= 10者用大寫字母
        # for process in processes:
        if method != 6:
            file.write(f"{meth[method-1]}" + "\n")
        else:
            file.write("Priority RR\n")
        if method == 2 :
            file.write("==          " + f"{meth[method-1]}==" + "\n") 
        elif method == 3 :
            file.write("==         " + f"{meth[method-1]}==" + "\n") 
        else :
            file.write("==        " + f"{meth[method-1]}==" + "\n")
        # 一張甘特圖
        file.write(Gantts[0] + "\n")
        file.write("===========================================================\n")


        # 印WT(依ID大小)
        file.write("\nWaiting Time\nID\t" + f"{meth[method-1]}\n")  
        file.write("===========================================================\n")
        for ID in WT:
            file.write( f"{ID}\t{WT[ID][method-1]}\n")   
        file.write("===========================================================\n")


        # 印TA(依ID大小)
        file.write("\nTurnaround Time\nID\t" + f"{meth[method-1]}\n")
        file.write("===========================================================\n")
        for ID in TA:
            file.write(f"{ID}\t{TA[ID][method-1]}\n")
        file.write("===========================================================\n\n")


if method == 7:
    outputfile = "out_" + f"{filename[:6]}" + ".txt"
    with open(outputfile, "w") as file:
        file.write("All\n")
        for i in range(6):
            if i == 1 :
                file.write("==          " + f"{meth[1]}==" + "\n") 
            elif i == 2 :
                file.write("==         " + f"{meth[2]}==" + "\n") 
            else :
                file.write("==        " + f"{meth[i]}==" + "\n")
            file.write(Gantts[i] + "\n")       # 甘特圖每張都appended兩次???!!!!因為妳寫了兩次append

        file.write("===========================================================\n")

        # 印WT(依ID大小)
        file.write("\nWaiting Time\nID\tFCFS\tRR\tSJF\tSRTF\tHRRN\tPPRR\n")
        file.write("===========================================================\n")
        for ID in WT:
            file.write(f"{ID}\t")
            for i in range(1, 7):
                file.write(f"{WT[ID][i-1]}")
                if i < 6:
                    file.write("\t") 
            file.write("\n")
        file.write("===========================================================\n")

        # 印TA(依ID大小)
        file.write("\nTurnaround Time\nID\tFCFS\tRR\tSJF\tSRTF\tHRRN\tPPRR\n")
        file.write("===========================================================\n")
        for ID in TA:
            file.write(f"{ID}\t")
            for i in range(1, 7):
                file.write(f"{TA[ID][i-1]}")
                if i < 6:
                    file.write("\t") 
            file.write("\n")
        file.write("===========================================================\n")

