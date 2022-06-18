def generate_exclusion_list(hls_input_file,exclusion_list_file):
    file_lines = []
    with open(hls_input_file,'r') as input_file:
        file_lines = input_file.readlines()

    r_list = []
    with open(hls_input_file,'w') as clean_code:
        for i,x in enumerate(file_lines):
            if "@" in x:
                if "loop_ignore" in x:
                    r_list.append(f"{i+1+1}\n")
                clean_code.write(f"//{x}")
            else:
                clean_code.write(x)

    with open(exclusion_list_file,'w') as exf:
        exf.write(f"{len(r_list)}\n")
        for l in r_list:
            exf.write(l)




