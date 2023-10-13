import torch
import time

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(torch.cuda.current_device()))


def fn(x, y):
    a = torch.cos(x).cuda()
    b = torch.sin(y).cuda()
    return a + b


"""for i in range(31):
    start = time.time()
    new_fn = torch.compile(fn, backend="inductor")
    input_tensor = torch.randn(2 ** i).to(device="cuda:0")
    a = new_fn(input_tensor, input_tensor)
    finish = time.time()
    #print(finish - start)
    print(round((finish - start)*1000)/1000,i,(finish - start)/(2 ** i)*(2**31),2**i)
"""
i=31
start = time.time()
new_fn = torch.compile(fn, backend="inductor")
input_tensor = torch.randn(1050000000).to(device="cuda:0")
a = new_fn(input_tensor, input_tensor)
finish = time.time()
#print(finish - start)
print(round((finish - start)*1000)/1000,i,(finish - start)/(2 ** i)*(2**31),2**i)