import metod

def main():
    c = [5.0, 6.0, 4.0, 1.0, 2.0, 3.0]

    a = [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        , [1.0, 3.0, 0.0, 2.0, -3.0, 1.0]
        , [0.0, 0.5, 4.0, 1.0, 0.0, 3.0]]

    b = [7.0, -8.0, 6.0]

    run = metod.Simplex(c, a, b)
    run.RunSimplex()

    print("Hi")

if __name__ == '__main__':
    main()