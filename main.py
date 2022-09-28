import re
import csv


# читаем адресную книгу в формате CSV в список contacts_list
def csv_file_to_list(filename):
    with open(filename, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


# 1. Отсекаем в записи, если есть пустой элемент с id=7. Т.к. шаблон csv - 7 элементов, а не 8.
def only_seven(contacts_list):
    contacts_list1 = []
    for person in contacts_list:
        if len(person) > 7:
            contacts_list1.append(person[:7])
        else:
            contacts_list1.append(person)
    del contacts_list
    return contacts_list1


# 2. Обрабатываем первые 3 элемента. Варианты:
# если Ф,И,О, или   Ф,И,, - то не обрабатываем
# если Ф И О,,, или  Ф И,,,   или   Ф,И О,,  - нужно обработать три варианта
def fio(contacts_list1):
    contacts_list2 = []
    for one_person_list in contacts_list1:
        if ' ' in one_person_list[0]:  # для случая Ф И О,,, или  Ф И,,,
            list1 = one_person_list[0].split()
            if len(list1) == 3:  # для случая Ф И О,,,
                contacts_list2.append(list1 + one_person_list[3:])
            elif len(list1) == 2:  # для случая Ф И,,,
                contacts_list2.append(list1 + one_person_list[2:])
        elif ' ' in one_person_list[1]:  # для случая Ф,И О,,
            contacts_list2.append([one_person_list[0]] + one_person_list[1].split() + one_person_list[3:])
        else:
            contacts_list2.append(one_person_list)
    del contacts_list1, list1  # Удаляем старый список.
    return contacts_list2


# Слияние двух списков. Вспомогательная функция для блока #3
def merge_lists(l1, l2):
    for k in range(2, len(l1)):
        if l1[k] == '':
            l1[k] = l2[k]
    return l1


# 3. Объединяем записи с одинаковыми Фамилия, Имя. Удаляем повторы после слияния.
def merge_contacts_list(contacts_list2):
    del_list = []  # список с индексами повторных записей для их последующего удаления
    n = len(contacts_list2)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if contacts_list2[i][:2] == contacts_list2[j][:2]:
                contacts_list2[i] = merge_lists(contacts_list2[i], contacts_list2[j])  # Слияние записей с одинаковыми ФИ
                del_list.append(j)  # Добавляем номер записи, которую нужно удалить
    # Удаление повторных записей после слияния
    offset = 0
    for i in del_list:
        i -= offset
        contacts_list2.pop(i)
        offset += 1
    return contacts_list2


# 4. Обработка телефонов
def re_phone(contacts_list2):
    pattern1 = r"(\+7|8)\s*\(*(\d{3})\)*\-*\s*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})\s*\(?(доб\.)?\s*(\d{4})?\)?\s*"
    substitution = r'+7(\2)\3-\4-\5 \6 \7'
    for i in range(len(contacts_list2)):
        contacts_list2[i][5] = re.sub(pattern1, substitution, contacts_list2[i][5]).strip()
    return contacts_list2


# код для записи файла в формате CSV
def list_to_csv_file(contacts_list2, filename):
    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list2)


if __name__ == '__main__':
    contacts_list_ = csv_file_to_list("phonebook_raw.csv")  # Формируем список из файла
    contacts_list_ = only_seven(contacts_list_)  # Оставляем только семь элементов согласно шаблону csv
    contacts_list_ = fio(contacts_list_)  # Обрабатываем ФИО. Обработка первых трёх позиций.
    contacts_list_ = merge_contacts_list(contacts_list_)  # Слияние одинаковых записей
    contacts_list_ = re_phone(contacts_list_)  # Обработка номеров телефонов согласно шаблону с помощью регулярок
    list_to_csv_file(contacts_list_, "phonebook.csv")  # Запись обработанного списка в csv файл
