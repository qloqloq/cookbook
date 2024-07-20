class HelloWorld:
    def hello(self):
        return 'Hello World.'


if __name__ == '__main__':
    greeting = HelloWorld().hello()
    print(greeting)