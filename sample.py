from visualdeploy import make_app

commands = ['echo {}sec; sleep {}'.format(i, 1) for i in range(0, 10)]

app = make_app(commands)

