import ctypes

lib = ctypes.CDLL(r'C:\Users\bakyt\source\repos\some_try\x64\Debug\some_try.dll')
arr1 = ctypes.c_int * 3
new_arr = ctypes.c_int * 3

size = ctypes.c_int(3)
t_arr1 = arr1(1, 2, 3)

t_new_arr = new_arr(lib.my_first_func(t_arr1, size))
print(*t_arr1)
print(*t_new_arr)  # <__main__.c_long_Array_3 object at 0x000002881F89AE40>
print(t_new_arr[0])  # random number
print(t_new_arr[1])  # 0
print(t_new_arr[2])  # 0
