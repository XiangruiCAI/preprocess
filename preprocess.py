#! /usr/bin/python
# encoding=utf-8

import csv
import os


IMAGEMALE = './IMAGE/DX 胸片 男/'
IMAGEFEMALE = './IMAGE/DX 胸片 女/'

num_male = 0
num_female = 0
num_pos = 0
num_neg = 0

LOG = open('preprocess.log', 'w')


def find_record(name):
    '''
    find the image path in the two folder
    name: the given folder name
    return image path and '' if no images found
    '''

    # print 'in find_record, name: ' + name
    prefix = ''
    if os.path.isdir(IMAGEMALE + name):
        prefix = IMAGEMALE + name
    elif os.path.isdir(IMAGEFEMALE + name):
        prefix = IMAGEFEMALE + name
    else:
        LOG.write('Image folder not found: ' + name + '\n')
        return ''

    images = os.listdir(prefix)
    if len(images) == 0:
        LOG.write('Image folder is empty: ' + prefix + '\n')
        return ''

    path = os.path.join(prefix, images[0])
    return path


def meta_data(iline):
    '''
    generate a line of the meta data for trainning
    list: a input line in the records.csv file
    return: a list containing path, label, IID, gender
    '''

    meta = []
    iid = iline[0].strip()
    uid = iline[1].strip()
    report_desc = iline[2].strip()
    study_desc = iline[3].strip()

    label = 1
    gender = 1
    if study_desc == '胸部正位片(DR)' or study_desc == '胸部正侧位片(DR)':
        # print 'hello, in study_desc'
        path = find_record(uid)
        # print 'path: ' + path
        if path == '':
            return meta

        if report_desc == '心肺膈未见明显异常。':
            label = 1
            num_pos += 1
        else:
            label = 0
            num_neg += 1

        if IMAGEMALE in path:
            gender = 1
            num_male += 1
        else:
            gender = 0
            num_female += 1

        meta.append(path)
        meta.append(label)
        meta.append(iid)
        meta.append(gender)

    return meta


if __name__ == '__main__':
    with open('./records.csv', 'rb') as csvinput, \
            open('./meta.csv', 'w') as csvoutput1,  \
            open('./meta_full.csv', 'w') as csvoutput2:
        RECORDS = csv.reader(csvinput)
        next(RECORDS, None)
        HEADER = ['path', 'label', 'IID', 'gender']

        OUT1 = csv.writer(csvoutput1, delimiter=' ')
        OUT2 = csv.writer(csvoutput2, delimiter=' ')
        OUT1.writerow(HEADER[:2])
        OUT2.writerow(HEADER)

        #count = 0
        for line in RECORDS:
            # print line
            metaline = meta_data(line)
            if metaline:
                OUT1.writerow(metaline[:2])
                OUT2.writerow(metaline)
            #count += 1
            # if count == 10: break
        if num_male + num_female != num_pos + num_neg:
            print "Error!"
        else:
            print "number of male: ", num_male
            print "number of female: ", num_female
            print "number of positive samples", num_pos
            print "number of negative samples", num_neg

    LOG.close()
