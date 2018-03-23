from main import word_lex_test, convert_out, parse


tests = ["(U)^3",
         "(V(t-1.1, {x, 0.7}))^3",
         "(D[V(t-1.1), {x, 2}])^3",
         '(U(t-1))^3',
         "D[U(t-1.1), {x,2}]+D[U(t-5.1), {y,2}]+D[V(t-1.1), {x,1}]",
         "-(U(t,{x, a}))",
         "-(U(t,{x, 0.7}))",
         "-(V(t-1.1, {x, a}))",
         "-(V+U)",
         "-(W(t, {x, 0.7}{y, 0.3}))",
         "-(U(t-1.1, {x, 0.7}{y, 0.3}))",
         "sin(x, y)*t",

         "U'=a+U+U*U*V-(b+1)*U+c*D[U,{x,2}]",
         "U'=a+U*U*V-(b+1)*U+c*D[U,{x,2}]",
         "U",
         "U'=a+U*U*V-(b+1)*U+c*D[U,{x,2}]",
         "U'=a+U*U*V-(b+1)*U+c*(D[U,{x,2}]+D[U,{y,2}])",
         "U'=a+U*U*V-(b+1)*U+c*(D[U,{x,2}]+D[U,{y,2}])",
         "U'= a * D[U,{x,2}]",
         "U'= a * (D[U,{x,2}] + D[U,{y,2}])",
         "U'= a * (D[U,{x,2}] + D[U,{y,2}])",
         
         "U'= a * (D[U,{x,2}] + D[U,{y,2}])",
         "U'= a * (D[U,{x,2}] + D[U,{y,2}])",
         "U'= 0",
         "U'= b * (D[U,{x,2}] + D[U,{y,2}])",
         "U'= a * (D[U,{x,2}] + D[U,{y,2}])",
         "U'=a*(D[U,{x,2}] + D[U,{y,2}])",
         "U'=a*(D[U,{x,2}] + D[U,{y,2}])",
         "U'=a*(D[U,{x,2}] + D[U,{y,2}])",
         "U'= D[U,{x,2}]",
         "U'=a*D[U,{x,2}]+ r*U*(1-U(t-1))",
         "U'=a*D[U,{x,2}]+ r*U*(1-U(t-1))",
         "U'= D[U,{x,2}] + D[V,{x,2}]",
         "U'=a*D[U,{x,2}] + d*U",
         "U(t,{x,0.7})",
         "U'=a*D[U,{x,2}]",
         "U'=a*(D[U,{x,2}] + D[U,{y,2}])",
         "U'=a*(D[U,{x,2}]+D[U,{y,2}])+U(t-3.1)+U(t-1.3)",
         "U'= D[U,{x,2}]",
         "U'=2.0 - V",
         "(U(t-1.3,{x, 0.7}{y,0.3}))",
         "U'=a*(D[U,{x,2}] + D[U,{y,2}])",
         "U",
         "U'=a * (D[U,{x,2}] + D[U,{y,2}])",
         "U'=b * (D[U,{x,2}] + D[U,{y,2}])",
         "U'=a+U*U*V-(b+1)*U+c*(D[U,{x,2}]+D[U,{y,2}])",
         "U'=t1 * (D[U,{x,2}] + D[U,{y,2}])",
         "U'=2.0 - V",
         "U'=a*(D[U,{x,2}] + D[U,{y,2}])"]


def test_parser(sent):
    try:
        result = word_lex_test(sent)
    except:
        result = None
    return(result)


def test():
    
    tests_1 = [(lambda sent: sent.replace(' ', ""))(test.split('=')[-1])
               for test in tests]
    print(tests_1)
    
    results = [test_parser(sent) for sent in tests_1]
    
    for _id, result in enumerate(results):
        print("\ntest: %s" % (tests_1[_id]))
        if result is not None:
            # print("\nresult tree:")
            # print(result)
            print("\nconverted:")
            print(result)
            # print(convert_out(result))
        else:
            print('fail')


def parse_one(test):
    #return(parse(test))

    try:
        return(parse(test))
    except:
        return(None)

    
def test_new():
    res = [parse_one(test) for test in tests]
    for _id, result in enumerate(res):
        print("\ntest %s: %s" % (_id, tests[_id]))
        if result is not None:
            print("\nconverted:")
            print(result)
        else:
            print('fail')


if __name__ == '__main__':
    # test()
    test_new()
