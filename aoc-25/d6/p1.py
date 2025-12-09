input = [nums for nums in open("input.txt").read().splitlines()]
nums_one = list(map(int, input[0].split()))
nums_two = list(map(int, input[1].split()))
nums_three = list(map(int, input[2].split()))
nums_four = list(map(int, input[3].split()))

operators = input[4].split()

total = 0
for i in range(len(nums_one)):
    if operators[i] == '*':
        total += nums_one[i] * nums_two[i] * nums_three[i] * nums_four[i]
    else:
        total += nums_one[i] + nums_two[i] + nums_three[i] + nums_four[i]
print(total)