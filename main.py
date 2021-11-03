import zipfile
import os
import hashlib
import requests
import re
import csv


if __name__ == '__main__':

    directory_to_extract_to = 'C:\\Users\\wgrag\\Desktop\\Прик.прог\\Лабораторная 1'        # 1
    arch_file = 'C:\\Users\\wgrag\\Downloads\\tiff-4.2.0_lab1.zip'
    os.mkdir(directory_to_extract_to)
    arch_file = zipfile.ZipFile(arch_file)
    arch_file.extractall(directory_to_extract_to)
    arch_file.close()


    txt_files = []                                                                          #2
    for r, d, f in os.walk(directory_to_extract_to):
        for i in f:
            if ".txt" in i:
                txt_files.append(os.path.join(r, i))
    for i in txt_files:
        print(i)


    for file in txt_files:
        tar_file_data = open(file, "rb")
        data = tar_file_data.read()
        result = hashlib.md5(data).hexdigest()
        tar_file_data.close()


    print("Значения MD5 хеша для найденных файлов: ")
    print(result)

    target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"                                        #3
    target_file = ''
    target_file_data = ''
    for r, d, f in os.walk(directory_to_extract_to):
        for i in f:
            file = open(os.path.join(r, i), 'rb').read()
            file_data = hashlib.md5(file).hexdigest()
            if file_data == target_hash:
                target_file = os.path.join(r, i)
                target_file_data = file

    print("Путь к файлу: ")
    print(target_file)
    print("Содержимое файла: ")
    print(target_file_data)

    r = requests.get(target_file_data)                                                          #4
    result_dct = {}
    counter = 0
    lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
    for line in lines:
        if counter == 0:
            headers = re.sub(r'<[^<>]*>', ' ', line)
            headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
        temp = re.sub(r'<[^<>]*>', ';', line)
        temp = re.sub(r'[*]', '', temp)
        temp = re.sub(r'\(.*?\)', '', temp)
        temp = re.sub(';[;;]*;', ';', temp)
        temp = re.sub(r'^\W+', '', temp)
        temp = re.sub('_', '-1', temp)
        temp = re.sub(r'\xa0', '', temp)
        tmp_split = re.split(';', temp)
        if counter != 0:
            country_name = tmp_split[0]
            col1_val = tmp_split[1]
            col2_val = tmp_split[2]
            col3_val = tmp_split[3]
            col4_val = tmp_split[4]
            result_dct[country_name] = [0, 0, 0, 0]
            result_dct[country_name][0] = int(col1_val)
            result_dct[country_name][1] = int(col2_val)
            result_dct[country_name][2] = int(col3_val)
            result_dct[country_name][3] = int(col4_val)
        counter += 1



    output = open('data.csv', 'w')                                                                        #5
    writer = csv.writer(output, delimiter=";")
    writer.writerow(headers)
    for key in result_dct.keys():
        writer.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
    output.close()

    target_country = input("Введите название страны: ")                                                 #6
    print(result_dct[target_country])
