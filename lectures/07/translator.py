CODE = '''
push constant 16384   // смещение начала экрана, 16384
pop pointer 1         // база сегмента that
push constant 32767   // закрасить 16 пикселей целиком
pop that 4000         // примерно в середину экрана
'''.strip()

def emit(instructions):
    for line in instructions.split(', '):
        print(line)

def pop_stack_to_d():
    emit('@SP, M=M-1, A=M, D=M')

def init_stack():
    emit('@256, D=A, @SP, M=D')

init_stack()

for line in CODE.split('\n'):
    if '//' in line:
        line = line.split('//')[0]
    command, *args = line.strip().split()
    if command == 'push':
        segment, offset = args
        if segment == 'constant':
            emit('@{0}, D=A, @SP, A=M, M=D, @SP, M=M+1'.format(offset))
    elif command == 'pop':
        segment, offset = args
        if segment == 'pointer':
            pop_stack_to_d()
            emit('@{}, M=D'.format(['THIS', 'THAT'][int(offset)]))
        elif segment == 'that':
            # *(*THAT + 4000) := **SP

            # THAT == 4
            # *THAT == 16384
            # D := *THAT + 4000 == 20384
            emit('@{0}, D=M, @{1}, D=A+D'.format(segment.upper(), offset))

            # *R13 := D
            emit('@R13, M=D')

            # SP == 0
            # *SP == 256
            # D := **SP == 32767
            pop_stack_to_d()

            # **R13 := D
            emit('@R13, A=M, M=D')
