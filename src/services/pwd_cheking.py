spec_simvols = ['.', ',', '<', '>', '/', '?', '|', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '±',
                '_', '-', '+', '=', ';', ':', '`', '~']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


async def pwd_check(password):
    n = 0
    n += 1 if len(password) >= 8 else 0
    n += 1 if password.lower() != password else 0
    for i in spec_simvols:
        if i in password:
            n += 1
            break
    for i in numbers:
        if i in password:
            n += 1
            break
    if n == 4:
        return 'отличый🟢'
    elif n == 3:
        return 'надежный🟡'
    else:
        return 'ненадежный🔴'