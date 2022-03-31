def loop_pragma_generator(pipeline=False, II = 1, unroll=False, factor=2):
    pragma_list = []
    if(pipeline and II > 0) :  
        string = "#pragma HLS pipeline II=" + str(II)
        pragma_list.append(string)
    if(unroll and factor > 1) : 
        string = "#pragma HLS unroll factor=" + str(factor)
        pragma_list.append(string)
    return pragma_list


def array_pragma_generator(variable,partition=False,mode='block',factor=2,dimension=1):
    if partition and factor > 1:
        pragma = f"#pragma HLS array_partition variable={variable} {mode} factor={factor} dim={dimension}"
        return [pragma]
    return []
