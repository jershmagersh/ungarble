"""
Pattern of our call to slicebytetostring after each deobfuscation
sequence.
00482999  xor     eax, eax  {0x0}
0048299b  lea     rbx, [rsp+0x6d {var_93}]
004829a0  mov     ecx, 0x2e
004829a5  call    sub_4461e0
"""
def check_slicebytetostr(finstrs, i):
    if finstrs[i-1][0][0].text == 'mov' \
    and finstrs[i-1][1] == 5 \
    and finstrs[i-2][0][0].text == 'lea' \
    and finstrs[i-2][1] == 5:
        return True
    else:
        return False

"""
Disassembled instructions are nested lists, so we need
to enumerate all nested tokens to find if a specific type exists.
"""
def match_nested_type(disas_instr, disas_type):
    for i in disas_instr:
        for j in i:
            if isinstance(j, disas_type):
                return True
    return False

"""
009da72f  4881ec90000000     sub     rsp, 0x90
009da736  4889ac2488000000   mov     qword [rsp+0x88 {__saved_rbp}], rbp
009da73e  488dac2488000000   lea     rbp, [rsp+0x88 {__saved_rbp}]
009da746  48ba416816241723…mov     rdx, 0x7774231724166841
"""
def match_disas_adv_seq_func_only(f):
    #Collect all potential start and end addresses
    taddr = []
    curr_start = 0
    for bb in f.basic_blocks:
        finstrs = list(bb)
        for i, instr in enumerate(finstrs):
            # This pattern may seem simplistic, but
            # having generic enough patterns is difficult
            # and using ILs is not always feasible due to
            # the complexity of Golang functions.
            try:
                if instr[0][0].text == 'mov' \
                and len(instr[0]) == 5 \
                and instr[0][4].value > 0xFFFF \
                and finstrs[i+1][0][0].text == 'mov' \
                and len(finstrs[i+1][0]) == 12 \
                and finstrs[i+2][0][0].text == 'mov' \
                and len(finstrs[i+2][0]) == 5 \
                and finstrs[i-1][0][0].text != 'mov':
                    # Resolve current address from
                    # instruction lengths embedded
                    # within each instruction
                    curr_start = bb.start
                    for j in range(0, i):
                        curr_start += bb[j][1]
    
                if instr[0][0].text == 'call':
                    if check_slicebytetostr(finstrs, i) and curr_start != 0:
                        print(f"Identified potential obf func: 0x{curr_start:2x}")
                        eaddr = bb.start
                        for j in range(0, i):
                            eaddr += bb[j][1]
                        taddr.append({'start': curr_start, 'end': eaddr})
                        curr_start = 0
            except:
                pass
    return taddr

def run_container_vstack(container_name, sample, start_address, stop_address):
    cmd = ["/usr/local/bin/docker", "exec", container_name,
           "bash", "/scripts/vstack.sh", sample, str(start_address), str(stop_address)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    rstr = result.stdout
    return rstr

def start_container(container_name):
    print("[+] Starting container")
    subprocess.run(["/usr/local/bin/docker", "run", "--rm", "-d", "--name", container_name, "ubuntu-ungarble", "sleep", "infinity"])

def stop_container(container_name):
    print("[+] Stopping container and removing")
    subprocess.run(["/usr/local/bin/docker", "stop", container_name])
    subprocess.run(["/usr/local/bin/docker", "rm", container_name])

def main():
    start_container("ungarble")
    taddr = []
    for f in bv.functions:
        taddr.extend(match_disas_adv_seq_func_only(f))
    f = bv.get_function_at(0x00b002a0)
    print(match_disas_adv_seq_func_only(f))
    for seq in taddr:
        print(f"Emulating at 0x{seq['start']:2x} and ending at 0x{seq['end']:2x}")
        rstr = run_container_vstack("ungarble", "3bd98de6361abdc0b7701e5b134879db841e00d4a64c3e517cf9becf2ed4ddea.bin", seq['start'], seq['end'])
        print(f"Resulting string: {rstr}")
    stop_container("ungarble")

def test():
    start_container("ungarble")
    f = bv.get_function_at(0x00b002a0)
    taddr = []
    taddr.extend(match_disas_adv_seq_func_only(f))
    for seq in taddr:
        print(f"Emulating at 0x{seq['start']:2x} and ending at 0x{seq['end']:2x}")
        rstr = run_container_vstack("ungarble", "3bd98de6361abdc0b7701e5b134879db841e00d4a64c3e517cf9becf2ed4ddea.bin", seq['start'], seq['end'])
        print(f"Resulting string: {rstr}")
    stop_container("ungarble")

main()
