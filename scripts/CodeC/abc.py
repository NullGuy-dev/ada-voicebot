# import json
# with open("intents.json", encoding="utf8") as file:
#     data = json.load(file)
# for i, val in enumerate(data['data']):
#     if val['tag'] == "code":
#         print(data['data'][i]['patterns'])
#         var = input("> ")
#         if var == "d":
#             while True:
#                 data1 = input()
#                 if data1 == ";":
#                     break
#                 print(data['data'][i]['patterns'].index(data1))
#                 del data['data'][i]['patterns'][data['data'][i]['patterns'].index(data1)]
#                 print(data['data'][i]['patterns'])
#         else:
#             while True:
#                 data1 = input()
#                 if data1 == ";":
#                     break
#                 data['data'][i]['patterns'].append(data1)
# print(data['data'][i]['patterns'])
# data = [
#     '''print("Hello, world!")''',
#     '''a = 2
#         b = 3
#         print(a + b)''',
#     '''x = 5
#         print(x ** 2)''',
#     '''n = 5
#         factorial = 1
#         for i in range(1, n+1):
#             factorial *= i
#         print(factorial)''',
#     '''n = 10
#         a, b = 0, 1
#         while a < n:
#             print(a)
#             a, b = b, a+b''',
#     '''s = "hello"
#         print(s[::-1])''',
#     '''n = 7
#         for i in range(2, n):
#             if n % i == 0:
#                 print("Not prime")
#                 break
#         else:
#             print("Prime")''',
#     '''s = "racecar"
#         if s == s[::-1]:
#             print("Palindrome")
#         else:
#             print("Not palindrome")''',
#     '''numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
#         numbers.sort()
#         print(numbers)''',
#     '''numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
#         print(sum(numbers))'''
# ]
# print(data,"\n\n\n\n\n")
# for i, el in enumerate(data):
#     data[i] = el.replace("\n","")
# print(data)
# with open("sfdfsdf", "w", encoding="utf8") as file:
#     file.write(str(data))
data = ''''''
data = data.replace("\n","")
with open("sfdfsdf", "w", encoding="utf8") as file:
    file.write(data)
