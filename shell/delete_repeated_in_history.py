import re


def rewrite_history(history_file, copy_history=True):
    print(history_file)

    with open(history_file, 'rb') as f:
        history = f.read()

    if copy_history:
        with open(history_file + '1', 'wb') as f:
            f.write(history)

    lines_commands = {}
    for history_command in history.split(b'\n: '):
        line_id = re.findall(b'\d+:0;', history_command)[0]
        command = history_command.split(line_id)[-1].strip().rstrip(b'\\')

        if not command:
            continue

        try:
            command.decode(encoding='utf-8')
        except UnicodeDecodeError:
            continue

        lines_commands[command.strip()] = line_id

    with open(history_file, 'wb') as f:
        for command, line_id in sorted(lines_commands.items(), key=lambda line: line[1]):
            f.write(b': ' + line_id + command + b'\n')


if __name__ == '__main__':
    rewrite_history('/Users/n.korolkov/.zsh_history')  # echo $HISTFILE
