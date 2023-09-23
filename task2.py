# Задание 1.
# Условие:
# Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
# *Задание 2. *
# • Установить пакет для расчёта crc32
# sudo apt install libarchive-zip-perl
# • Доработать проект, добавив тест команды расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.
import subprocess

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    # print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False

def checkout_negative(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    # print(result.stdout)
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False

folder_in = "/home/semgen/tst"
folder_out = "/home/semgen/out"
folder_ext = "/home/semgen/folder1"
folder_bad = "/home/semgen/folder2"

def test_step1():
    # test1
    assert checkout_negative(f"cd {folder_bad};  7z e arx2.7z -o{folder_ext} -y", "ERRORS"), "test1 FAIL"


def test_step2():
    # test2
    assert checkout_negative(f"cd {folder_bad}; 7z t arx2.7z", "ERRORS"), "test2 FAIL"

def test_step3():
    # test3
    assert checkout(f"cd {folder_out}; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout(f"cd {folder_out}; 7z d arx2.7z", "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    assert checkout(f"cd {folder_in}; 7z u {folder_out}/arx2.7z", "Everything is Ok"), "test5 FAIL"

def test_step6():
    # test6
    res1 = checkout(f"cd {folder_in};  7z a {folder_out}/arx2", "Everything is Ok")
    res2 = checkout(f"ls {folder_out}", "arx2.7z")
    assert res1 and res2, "test6 FAIL"

def test_step7():
    # test7
    res1 = checkout(f"cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y", "Everything is Ok"), "test7 FAIL"
    res2 = checkout(f"ls {folder_ext}", "test1.txt")
    res3 = checkout(f"ls {folder_ext}", "test2.txt")
    assert res1 and res2 and res3, "test7 FAIL"

# Задание 1.

def test_list_files():
    #test8
    assert checkout(f"cd {folder_out}; 7z l arx2.7z", "0 files")

def test_extract_files():
    #test9
    subprocess.run(f"7z a {folder_ext}/tst.7z {folder_ext}/test1.txt {folder_ext}/test2.txt", shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    assert checkout(f"7z x {folder_ext}/tst.7z -y", "Files: 2")

# *Задание 2. *

def test_crc32_compare_h7z():
    crc = subprocess.run(f"crc32 {folder_ext}/tst.7z {folder_ext}/test1.txt {folder_ext}/test2.txt", shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8').stdout.upper().split()[0]
    assert checkout(f"7z h {folder_ext}/tst.7z", crc)