import pandas as pd


data_column = pd.read_excel(r"C:\Users\Administrator\Desktop\1.xlsx")["真新客期间累计消耗现金金额"]
nums_list = list(data_column)

# print(nums_list)

def has_subset_sum(nums, target=10000):
    result = []

    for num in nums:
        if num == 0:
            continue

        if num not in result:
            result.append(num)
            for i in range(len(result)-1):
                result[i] = result[i] + num
        else:
            for i in range(len(result)):
                result[i] = result[i] + num

        print(result)

        if target in result:
            return True

    return False

test = [1000, 2000, 3000, 4000, 5000]
print(has_subset_sum(test))
# print(has_subset_sum(nums_list))
