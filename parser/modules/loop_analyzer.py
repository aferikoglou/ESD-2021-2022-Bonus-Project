def contained(begin_l_end,begin_c_end,end_l_start,end_c_start):
    if (begin_l_end,begin_c_end) > (end_l_start,end_c_start):
        return True
    return False

def loop_analysis(ipt_file):

    with open(ipt_file,'r') as loop_lines:
        llines = loop_lines.readlines()

    fn_blocks = []
    i = 0
    while i < len(llines):
        tmp = []
        if "FND:" in llines[i]:
            fn_name = llines[i].split(":")[1]
            j = i + 1
            while j < len(llines) and "FND:" not in llines[j]:
                if "FNC:" not in llines[j]:
                    tmp.append(llines[j][:-1])
                j += 1
            i = j
            fn_blocks.append((fn_name[:-1],list(tmp)))

    function_loop_list = []

    for fn_block in fn_blocks:
        fn_name = fn_block[0]
        loop_list = fn_block[1]

        ll = []
        for loop in loop_list:
            loop_name = loop.split(":") [0] 
            vars = [int(x) for x in (loop.split(":")[1]).split(",")]
            ll.append((loop_name,*vars))

        loop_level = [0 for x in ll]
        for i,x in enumerate(ll):
            for k in range(i+1,len(ll)):
                if contained(x[3],x[4],ll[k][1],ll[k][2]): loop_level[k] += 1
                else: break

        loop_information = [(ll[i][0],x,list()) for i,x in enumerate(loop_level)]

        for i,x in enumerate(loop_information):
            for k in range(i+1,len(loop_information)):
                if x[1]+1 == loop_information[k][1]:
                    x[2].append(k)

        function_loop_list.append((fn_name,loop_information))

    return function_loop_list






