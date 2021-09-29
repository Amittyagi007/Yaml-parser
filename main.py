import re
import os
import yaml

from yaml.loader import SafeLoader
from collections import OrderedDict

import conf


def readYaml():
    """This function opens the given yaml file and loads it's data
        parameters : none
        returns : NA"""
    try:
        with open(conf.yaml_file_location) as f:
            data = yaml.load(f, Loader=SafeLoader)
            getVals(data)
    except Exception as e:
        print("Something went while reading the yaml file")


def recursive_items(dictionary):
    """This function iterates through the nested items of dictionary
        parameters : dictionary
        returns : yieled keys and values"""
    try:
        for key, value in dictionary.items():
            if type(value) is dict:
                yield (key, value)
                yield from recursive_items(value)
            else:
                yield (key, value)
    except Exception as e:
        print("Something went while parsing the nested part of dictionary")


def writeYaml(s):
    """This function writes the final output to a fstab file
        parameters : string to be placed in the file
        returns : NA"""
    try:
        file = open(conf.fstab_file_location, 'a')
        file.write("\n" + s + "\n")
        file.close()
    except Exception as e:
        print("Something went while writing the fstab file")


def createString(lst):
    """This function iterates through the list and modifies it as required
        parameters : list
        returns : NA"""
    try:
        re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        str = ' '.join(lst)
        chk_nfs = str.split(' ')[0]
        mount_pnt = str.split(' ')[1]

        if re_ip.match(chk_nfs):
            lst = list(str.split(" "))
            lst[0], lst[3] = lst[0] + ':' + lst[3], lst[1]
            lst.remove(lst[1])
            str = ' '.join(lst)
            mount_pnt = 'nfs'

        if mount_pnt == '/':
            add = 'defaults 0 1'
        elif mount_pnt == '/home':
            add = 'defaults 0 2'
        elif mount_pnt == 'nfs':
            add = 'defaults 0 0'
        else:
            add = 'defaults 0 3'

        str = str + add
        writeYaml(str)
    except Exception as e:
        print("Something went while creating the string")


def getVals(data):
    """This function iterates through the dictionary and process the data. It also launches a command on OS for root-reserve param
        parameters : dictionary
        returns : NA"""
    try:
        for k1, v1 in data.items():  # the basic way
            for k2, v2 in v1.items():
                params = []
                current_mount = ''
                for k3, v3 in recursive_items(v2):
                    if k3 == 'mount':
                        current_mount = v3
                    if k3 == 'root-reserve':
                        cmd = 'sudo mkfs.ext4 -m %s %s' % (v3, current_mount)
                        # print(cmd)
                        os.system(cmd)
                        continue
                    params.append(str(k2))
                    if type(v3) is list:
                        v3 = ','.join(v3)
                        params.append(str(v3 + ','))
                    else:
                        params.append(str(v3 + ' '))
                params = list(OrderedDict.fromkeys(params))
                createString(params)
    except Exception as e:
        print("Something went while parsing the main dictionary")


def main():
    """This functions calls the readYaml function, which in turn starts the process of yaml parsing.
        parameters : NA
        returns : NA"""
    readYaml()


if __name__ == "__main__":
    main()
