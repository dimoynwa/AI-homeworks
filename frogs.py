def next_array_generator(array):
    length = len(array)
    for i in range(length):
        if array[i] == '>' and i + 1 < length and array[i+1] == '_':
            new_array = array[:]
            new_array[i], new_array[i+1] = new_array[i+1], new_array[i]
            yield new_array
        elif array[i] == '>' and i+2 < length and array[i+2] == '_':
            new_array = array[:]
            new_array[i], new_array[i+2] = new_array[i+2], new_array[i]
            yield new_array
        elif array[i] == '<' and i-1 >= 0 and array[i-1] == '_':
            new_array = array[:]
            new_array[i], new_array[i-1] = new_array[i-1], new_array[i]
            yield new_array
        elif array[i] == '<' and i-2 >= 0 and array[i-2] == '_':
            new_array = array[:]
            new_array[i], new_array[i-2] = new_array[i-2], new_array[i]
            yield new_array


def print_array(array):
    for i in range(len(array)):
        if i < len(array) - 1:
            print(array[i], end='')
        else:
            print(array[i])


def print_result(result):
    for array in result:
        print_array(array)


def frog_task(array, goal_array, result):
    for arr in next_array_generator(array):
        if arr == goal_array:
            result.append(arr)
            print_result(result)
            return result
        res = result[:]
        res.append(arr)
        res1 = frog_task(arr, goal_array, res)
        if res1:
            return res1


def generate_start_and_goal_arrays(number):
    start_array = []
    goal_array = []
    for i in range(number):
        start_array.append('>')
        goal_array.append('<')
    start_array.append('_')
    goal_array.append('_')
    for i in range(number):
        start_array.append('<')
        goal_array.append('>')
    return start_array, goal_array


if __name__ == '__main__':
    number = 0
    flag = True
    while flag:
        try:
            number = input()
            flag = False
            s, e = generate_start_and_goal_arrays(int(number))
            a = frog_task(s, e, [s])
        except Exception as e:
            flag = True
            print('Wrong input! Try again!')
