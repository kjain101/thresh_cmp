#Script to create event code with thresh_cmp value
#!/usr/bin/python
#

#Max latency for thresholding
MAX_LATENCY = 130048

#Number of bits for thresh cmp exponent and mantissa
THRESH_CMP_EXP  = 3
THRESH_CMP_MANTISSA = 7

def get_threshold(latency, event_code):
    exp = 0
    mant = 0
    mask = 0x1FF80
    check_mask = 0x60
    thresh_cmp = latency

    while(thresh_cmp & mask):
        thresh_cmp = thresh_cmp >> 2
        exp += 1
    mant = thresh_cmp

    if ((exp != 0) and not(mant & check_mask)):
        print("Unexpected error: Upper two bits of mant is 0s\n");
        exit()

    print("Thresh_cmp value = " + str(latency) + " : Mantissa = " +
            str(hex(mant)) + " and Exponent = " + str(hex(exp)) + "\n")

    thresh_cmp = (exp << THRESH_CMP_MANTISSA) | mant;

    event_code_thresh_mask = thresh_cmp << (63 - 23)

    #resultant event code
    event_code |= event_code_thresh_mask
    print(" Resultant event code = " + str(hex(event_code)))

    #perf script command
    print("\n*********************************************************************************\n")
    print(" Use command: 'perf record --weight -e cpu/event=" + str(hex(event_code)) + "/ <workload>'")
    print("\n*********************************************************************************\n")

print("\n")
eventcode = input("Input event code in hex: ")
thresh_cmp = input("Input threshold latency in decimal: ")
print("\n")

eventcode = int(eventcode, 16) # parse string into an hex
thresh_cmp = int(thresh_cmp) # parse string into an integer

if thresh_cmp > MAX_LATENCY:
    print("Error: Max latency supported by hardware is : %d\n", MAX_LATENCY)
    print("Try with smaller value\n")

get_threshold(thresh_cmp, eventcode);

