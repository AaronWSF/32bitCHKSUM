#!/usr/bin/python
import sys
import os
import multiprocessing as mp

def splitfile(filename):
    #get the file status information
    filesize = os.stat(filename).st_size
    
    #The slice number of the file we want to divide
    piece_num = 4
    
    originalfile = open(filename, 'rb')
    div_filesize = int(filesize/piece_num)
    i = 0
    #divided binary file into 4 parts
    while filesize >=1:
        read_content = originalfile.read(div_filesize)
        part_filename = str(i)+'.bin'
        with open(part_filename, 'wb') as file:
            file.write(read_content)
            file.close()
        i+=1
        if (filesize >=div_filesize):
            filesize -=div_filesize            
    originalfile.close()
    return i

def job(q, filename):
    sum =0
    part_filepath=(os.path.realpath(filename))
    #print (part_filepath)
    with open(part_filepath, 'rb') as f:
        f.seek(0)
        while True:
                byte = f.read(1)
                if not byte:
                    break
                sum += ord(byte)
        q.put(sum)
    
def calc32bitchecksum(slice):
    q = mp.Queue()
    p = list()
    res = list()
    sum = 0
    
    for i in range(0, slice, 1):
        slice_filename = str(i)+'.bin'
        p.append(mp.Process(target=job, args=(q,slice_filename)))
    
    for j in range(0, slice, 1):
        p[j].start()
        p[j].join()
    
    for m in range(0, slice, 1):
        res.append(q.get())

    for n in range(0, slice, 1):
        sum = sum + res[n]
    
    sum_string = str(hex(sum))
    sum_string = '0x'+sum_string[-8:].upper()
    
    #Delete the slice files
    for i in range(0, slice, 1):
        slice_filename = str(i)+'.bin'
        if os.path.isfile(slice_filename):
            os.remove(slice_filename)
        
    print('The checksum is ' + sum_string)


if __name__ == '__main__':
    # Due to use pyinstaller to wrap into exe file,
    # so it need to add below
    mp.freeze_support()
    slice_number = splitfile(os.path.realpath(sys.argv[1]))
    calc32bitchecksum(slice_number)
