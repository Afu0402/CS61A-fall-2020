big_limit = 10

# s -> sing
def test(start, goal):
    if start == goal:
        return 0
    start = [""] + list(start)
    goal = [""] + list(goal)
    start_length = len(start)
    goal_length = len(goal)

    dp = []
    dp.append(list(range(start_length)))

    init_index = 1
    while init_index < goal_length:
        init_arr = ["" for _ in range(start_length)]
        init_arr[0] = init_index
        dp.append(init_arr)
        init_index += 1
    print(dp)
    i = 1
    j = 1
    while i < goal_length:
        j = 1
        while j < start_length:
            current_min = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
            print("compare", start[j], "vs", goal[i])
            if start[j] != goal[i]:
                dp[i][j] = current_min + 1
            else:
                dp[i][j] = dp[i - 1][j - 1]
            j += 1
        i += 1
    print(dp)

    return dp[goal_length - 1][start_length - 1]


print(test("speling", "spelling"))
