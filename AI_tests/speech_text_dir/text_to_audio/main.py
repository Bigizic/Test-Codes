#!/usr/bin/python3
""" """


def lang_checker():
    file_path = 'languages.txt'
    lang = input("Enter language >>> ")
    arr = []
    new_arr = []
    instructions = f'You selected {lang} Please pick from the following\n'
    bracket = True
    result = None

    with open(file_path, "r") as open_file:
        lines = open_file.readlines()
        for lin in lines:
            if lang in lin:
                arr.append(lin.strip('\n'))
        for ite in arr:
            if not ite.find('('):
                new_arr.append(ite)
                bracket = False
            else:
                pi = ite.replace('(', '').replace(')', '')
                pi.split(' ')[1:]
                new_arr.append(pi)
    if not new_arr:
        print("Can't fine {} Try another country/Language".format(lang))
        return
    if not bracket and len(new_arr) < 2:
        print(new_arr)
        result = new_arr
        return result

    if bracket is True:
        print(instructions)
        print(new_arr)
        if len(new_arr) < 2:
            new_lang = input("\nEnter in this format [{}]: "
                             .format(new_arr[0]))
            if new_lang in new_arr:
                print("You selected {}".format(new_lang))
                result = new_lang
                return result
            else:
                print("Error: please check your input")
                return
        else:
            new_lang = input("\nEnter in this format [{}]: "
                             .format(new_arr[1]))
            if new_lang in new_arr:
                print("You selected {}".format(new_lang))
                result = new_lang
                return result
            else:
                print("Error: Please check your input")
                return


me = lang_checker()
print(me)
