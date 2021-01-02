# import time
# import multiprocessing
#
#
# def basic_func(x):
#     if x == 0:
#         return 'zero'
#     elif x % 2 == 0:
#         return 'even'
#     else:
#         return 'odd'
#
#
# def multiprocessing_func(x):
#     y = x * x
#     time.sleep(2)
#     print('{} squared results in a/an {} number'.format(x, basic_func(y)))
#
#
# if __name__ == '__main__':
#     starttime = time.time()
#     pool = multiprocessing.Pool()
#     pool.map(multiprocessing_func, range(0, 10))
#     pool.close()
#     print('That took {} seconds'.format(time.time() - starttime))
import multiprocessing
import os
import time
from multiprocessing import Process

from tqdm import tqdm


def basic_func(x):
    if x == 0:
        return 'zero'
    elif x % 2 == 0:
        return 'even'
    else:
        return 'odd'


def multiprocessing_func(x):
    y = x * x
    time.sleep(2)
    print('{} squared results in a/an {} number'.format(x, basic_func(y)))


def ExtractDicomMetadata(subset, root, file, return_dict):
    time.sleep(2)
    # try:
    # # dcm = read_dicom(os.path.join(root, file))
    # # for tag in tags:
    # #     try:
    # #         d[tag].append(dcm[tag].value)
    # #     except KeyError:
    # #         d[tag].append(None)
    # # d['path'].append(os.path.join(root, file))
    # # d['subset'].append(subset)
    # except Exception as e:
    #     print(e)
    #     print(os.path.join(root, file))
    return_dict['subset'] = subset
    return_dict['root'] = root
    return_dict['file'] = file


if __name__ == '__main__':
    starttime = time.time()
    processes = []

    for root, dirs, files in os.walk(r"C:\Users\user\Downloads\AVCutter"):
        processes = []
        i = 0
        return_dict = {}
        # print(f"Creating Multiprocessing processes for having data in ")
        for j, file in enumerate(files):
            return_dict[j] = multiprocessing.Manager().dict()

            p = Process(target=ExtractDicomMetadata, args=(dirs, root, file, return_dict[j]))
            processes.append(p)
            p.start()
            i += 1
            if i > 3000:
                break
        # print(f"Executing processes for ")
        for process in tqdm(processes):
            process.join()
            print(return_dict.values())
    #
    #
    # for i in range(0, 10):
    #     p = multiprocessing.Process(target=multiprocessing_func, args=(i,))
    #     processes.append(p)
    #     p.start()
    #
    # for process in processes:
    #     process.join()

    print('That took {} seconds'.format(time.time() - starttime))

# import time
#
#
# def basic_func(x):
#     if x == 0:
#         return 'zero'
#     elif x % 2 == 0:
#         return 'even'
#     else:
#         return 'odd'
#
#
# starttime = time.time()
# for i in range(0, 10):
#     y = i * i
#     time.sleep(2)
#     print('{} squared results in a/an {} number'.format(i, basic_func(y)))
#
# print('That took {} seconds'.format(time.time() - starttime))
