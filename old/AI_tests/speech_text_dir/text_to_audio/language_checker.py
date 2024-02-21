#!/usr/bin/python3
""" """


def extra_checks(lang: str) -> str:
    arr = []
    file_path = 'languages.txt'
    with open(file_path, "r") as open_file:
        lines = open_file.readlines()
        for lin in lines:
            arr.append(lin.replace('\n', '').replace('(', '')
                       .replace(')', '').lower())
        if lang in arr:
            return (lang.split(' ')[0])
        else:
            return lang


if __name__ == '__main__':
    extra_checks()


def lang_checker():
    file_path = 'languages.txt'
    lan = input("Enter language >>> ")
    arr = []
    new_arr = []
    instructions = f'You selected {lan} Please pick from the following\n'
    bracket = True
    result = None
    lang = extra_checks(lan.lower())
    if len(lang) < 2:
        print("OOPs You enterd nothing")
        return

    with open(file_path, "r") as open_file:
        lines = open_file.readlines()
        for lin in lines:
            if lang in lin.lower():
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
        print("Can't find {} Try another country/Language".format(lang))
        return
    # for instance ZULU
    if not bracket and len(new_arr) == 1:
        print(new_arr)
        result = new_arr
        return result

    if bracket is True:
        print(instructions)
        print(new_arr)
        # for instance of English Nigeria
        if len(new_arr) < 2:
            word = ("\nEnter in this format [{}], without brackets: "
                    .format(new_arr[0]))
            new_lang = input(word)
            if new_lang in new_arr:
                # print("You selected {}".format(new_lang))
                result = new_lang
                return result
            else:
                print("Error: please check your language format")
                return
        else:
            word = ("\nEnter in this format [{}], without brackets: "
                    .format(new_arr[1]))
            new_lang = input(word)
            if new_lang in new_arr:
                # print("You selected {}".format(new_lang))
                result = new_lang
                return result
            else:
                print("Error: Please check your language format")
                return


if __name__ == '__main__':
    lang_checker()
