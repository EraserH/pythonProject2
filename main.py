import zipfile
import os
import hashlib
import re
import requests
import csv

directory_to_extract_to = 'D:\\unzippedDirectory'
arch_file = 'D:\\tiff-4.2.0_lab1.zip'

test_zip = zipfile.ZipFile(arch_file)
test_zip_files = test_zip.namelist()
print(test_zip_files)
test_zip.extractall(directory_to_extract_to)
test_zip.close()

#Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to. Сохранить полученный список в txt_files

txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        if (re.match(r"txt[.].+", i[::-1])):
            txt_files.append(r + "\\" + i)

print(txt_files, end = '\n\n')

#myFile = open(txt_files[0], 'r')
#print(myFile.read(100000))

fileHash = []
for file in txt_files:
    file_data = open(file, 'rb').read()
    fileHash.append(hashlib.md5(file_data).hexdigest())

print(fileHash)

target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = 'literally nothing'

for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        tmp = os.path.join(r, i)
        data = open(tmp, "rb")
        content = data.read()
        if hashlib.md5(content).hexdigest() == target_hash:
            target_file = r + "\\" + i
            target_file_data = content

# Отобразить полный путь к искомому файлу и его содержимое на экране

print("Файл с указанным хэшем")
print(target_file)
print(target_file_data)


r = requests.get(target_file_data)
result_dct ={} # словарь для записи содержимого таблицы
counter = 0

lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        headers = re.sub('<.*?>', ' ', line)
        # Извлечение списка заголовков
        headers = re.findall(r'Заболели|Умерли|Вылечились|Активные случаи', headers)
        headers.insert(0, "Страны")
        print(headers, end="\n\n")
    else:
        if counter == 1:
            print(line, end="\n\n")

        temp = re.sub('<.*?>', ';', line)
    #    print(temp)
        temp = re.sub("\(.*?\)", '', temp)
    #    print(temp)
        temp = re.sub(';+', ';', temp)
    #    print(temp)
        temp = temp[1: len(temp) - 1]
    #    print(temp)
        temp = re.sub('\s(?=\d)', '', temp)
    #    print(temp)
        temp = re.sub('(?<=\d)\s', '', temp)
    #    print(temp)
        temp = re.sub('\*', '', temp)
    #    print(temp)
        temp = re.sub('_', '-1', temp)
    #    print(temp)
    #    print("\n\n")

        # Разбитие строки на подстроки
        tmp_split = temp.split(';')

        if len(tmp_split) == 6: #последняя строка "всего"
            tmp_split.pop(0)

        # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
        country_name = tmp_split[0]
        country_name = re.sub('.*\s\s', '', country_name)

        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]

        # Запись извлеченных данных в словарь
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)

    counter += 1

# Задание №5
# Запись данных из полученного словаря в файл

output = open('data.csv', 'w')
w = csv.writer(output, delimiter=";")
w.writerow(headers)
for key in result_dct.keys():
    w.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()

# Задание №6
# Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)

target_country = input("Введите название страны: ")
print(result_dct[target_country])


"""<div class="Table-module_row__3TH83"><div class="Table-module_cell__EFKDW Table-module_white__gzvo0 Table-module_m__29G9r">🇺🇸  США</div><div class="Table-module_cell__EFKDW Table-module_white__gzvo0 Table-module_s__Vl_Eg">45&nbsp;953&nbsp;186 <span style="color:#5C5E62;font-size:10px">(+29&nbsp;302)</span></div><div class="Table-module_cell__EFKDW Table-module_white__gzvo0 Table-module_s__Vl_Eg">745&nbsp;668 <span style="color:#5C5E62;font-size:10px">(+291)</span></div><div class="Table-module_cell__EFKDW Table-module_white__gzvo0 Table-module_s__Vl_Eg">0*</div><div class="Table-module_cell__EFKDW Table-module_white__gzvo0 Table-module_s__Vl_Eg">_</div></div>"""