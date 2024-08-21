# Chuỗi đầu vào
input_string = 'ND:CT DEN:420723414049 MLKELOBH-250724-23:59:16 414049 (0833776989); tai Napas'

# Tách chuỗi thành danh sách các phần tử ngăn cách nhau bằng khoảng trống
result_list = input_string.split()
result_list = result_list[2].split('-')
result_list  = result_list[0]

# In ra danh sách kết quả
print(result_list)
