# import sys
#
# class Tee:
#     def __init__(self, out1, out2):
#         self.out1 = out1
#         self.out2 = out2
#
#     def write(self, *args, **kwargs):
#         self.out1.write(*args, **kwargs)
#         self.out2.write(*args, **kwargs)
#
#
#
# sys.stdout = Tee(open("./logs.txt", "w"), sys.stdout)
#
# print("hello")