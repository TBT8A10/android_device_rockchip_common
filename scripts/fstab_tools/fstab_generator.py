#!/usr/bin/env python
import sys
import getopt
import os
from string import Template

usage = 'fstab_generator.py -I <type: fstab/dts> -i <fstab_template> -p <block_prefix> -f <flags> -c <chained_flags> -s <sdmmc_device> -o <output_file>'

def main(argv):
    ifile = ''
    prefix = ''
    flags = ''
    fstab_file = ''
    vbmeta_part = ''
    sdmmc_device = ''
    avbpub_key = ',avb_keys=/avb/q-gsi.avbpubkey:/avb/r-gsi.avbpubkey:/avb/s-gsi.avbpubkey'
    type = 'fstab'
    chained_flags = ''
    dt_vbmeta = 'vbmeta {\n\
        compatible = "android,vbmeta";\n\
        parts = "vbmeta,boot,system,vendor,dtbo";\n\
    };'
    try:
        opts, args = getopt.getopt(argv, "hI:i:p:f:c:s:o:", ["IType","ifile","bprefix=","flags=","chained_flags","sdevice=","ofile="])
    except getopt.GetoptError:
        print (usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (usage)
            sys.exit(2)
        elif opt in ("-I", "--IType"):
            type = arg;
        elif opt in ("-i", "--ifile"):
            ifile = arg;
        elif opt in ("-p", "--block_prefix"):
            prefix = arg;
        elif opt in ("-f", "--flags"):
            flags = arg;
        elif opt in ("-c", "--chained_flags"):
            chained_flags = arg;
        elif opt in ("-s", "--sdmmc_device"):
            sdmmc_device = arg;
        elif opt in ("-o", "--ofile"):
            fstab_file = arg;
        else:
            print (usage)
            sys.exit(2)

    if prefix == 'none':
        prefix = ''
    if flags == 'none':
        flags = ''
    if chained_flags == 'none':
        chained_flags = ''

    # add vbmeta parts name at here
    list_flags = list(flags);
    pos_avb = flags.find('avb')
    if pos_avb >= 0:
        list_flags.insert(pos_avb + 3, '=vbmeta')
    else:
        dt_vbmeta = ''
        avbpub_key = ''

    vbmeta_part = "".join(list_flags)

    file_fstab_in = open(ifile)
    template_fstab_in = file_fstab_in.read()
    fstab_in_t = Template(template_fstab_in)

    if type == 'fstab':
        line = fstab_in_t.substitute(_block_prefix=prefix,_flags=flags,_flags_vbmeta=vbmeta_part,_flags_avbpubkey=avbpub_key,_flags_chained=chained_flags,_sdmmc_device=sdmmc_device)
    else:
        line = fstab_in_t.substitute(_boot_device=prefix,_vbmeta=dt_vbmeta,_flags=flags)

    if fstab_file != '':
        with open(fstab_file,"w") as f:
            f.write(line)
    else:
        print (line)

if __name__=="__main__":
    main(sys.argv[1:])
