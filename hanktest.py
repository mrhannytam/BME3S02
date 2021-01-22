def test():
    try:
        def pprint():
            print('I am function')

        pprint()
    except Exception as e:
        print(e)

test()
