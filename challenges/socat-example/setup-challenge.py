#!/usr/bin/env python3
import sys
import os
import re
import json

def main():

    # create flag
    flag = os.environ.get("FLAG")

    if flag is None or flag == "":
        print("Flag was not read from environment. Aborting.")
        sys.exit(-1)
    else:
        # Get hash part
        flag_rand = re.search("{.*}$", flag)
        if flag_rand == None:
            print("Flag isn't wrapped by curly braces. Aborting.")
            sys.exit(-2)
        else:
            flag_rand = flag_rand.group()
            flag_rand = flag_rand[1:-1]
            flag_rand = flag_rand.zfill(8)

    new_flag = "picoCTF{b3wa8r3_0g_9r07oty9e_pOI1u7LoN_" + flag_rand + "}"
    
    with open("/app/flag.txt", "w") as f:
        f.write(new_flag)

    # Create and update metadata.json
    metadata = {}
    metadata['flag'] = str(new_flag)
    json_metadata = json.dumps(metadata)
    
    with open("/challenge/metadata.json", "w") as f:
        f.write(json_metadata)

if __name__ == "__main__":
    main()