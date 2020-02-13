import os


def combine(data):
    global vcount, vncount, vtcount
    tempvcount, tempvncount, tempvtcount = 0, 0, 0
    newdata = []
    for line in data.split('\n'):
        if line.startswith('v '):
            tempvcount += 1
            newdata.append(line)
        elif line.startswith('vn '):
            tempvncount += 1
            newdata.append(line)
        elif line.startswith('vt '):
            tempvtcount += 1
            newdata.append(line)
        elif line.startswith('f '):
            newdata.append('f ' + ' '.join(['/'.join([str(y) for y in [int(x.split('/')[0])+vcount, int(x.split('/')[1])+vtcount, int(x.split('/')[2])+vncount]]) for x in line.split()[1:]]))
        else:
            newdata.append(line)
    vcount += tempvcount
    vncount += tempvncount
    vtcount += tempvtcount
    return newdata


for folder in os.listdir('obj'):
    global vcount, vncount, vtcount
    vcount, vncount, vtcount = 0, 0, 0
    for name in os.listdir(f'obj/{folder}'):
        obj = open(f'obj/{folder}/{name}.obj' if os.path.isdir(f'obj/{folder}/{name}') else f'obj/{folder}.obj', 'w')
        if os.path.isdir(f'obj/{folder}/{name}'):
            for file in os.listdir(f'obj/{folder}/{name}'):
                obj.write('\n'.join(combine(open(f'obj/{folder}/{name}/{file}').read())))
        elif os.path.isfile(f'obj/{folder}/{name}') and name.endswith('.obj'):
            obj.write('\n'.join(combine(open(f'obj/{folder}/{name}').read())))
