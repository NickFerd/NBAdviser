
from nbadviser import Handler
from nbadviser import strategies


def main():
    handler = Handler(strategies)
    handler.run()


if __name__ == '__main__':
    main()
