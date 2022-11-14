import logging
import re
import fileinput


# logger = logging.getLogger(__name__)


def sys_loggin(log_level, to_file, message):
    """
        This function is used to logging message in command line or in to the file
        :params -> log_level: login function level to use eg: debug, error...
                -> to_file: bool if not False the message is write to file else in the command line
                -> message: current logging message
    """

    log_function = ['debug', 'info', 'error', 'warning', 'critical']
    log_function = ['error', 'warning', 'critical']
    if to_file:
        logging.basicConfig(filename='logging.log', encoding='utf-8',
                            format='%(asctime)s %(levelname)s: %(message)s %(name)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)

    logger = logging.getLogger(__name__)
    if log_level in log_function:
        if log_level == 'debug':
            logger.debug(message)
        if log_level == 'info':
            logger.info(message)
        if log_level == 'warning':
            logger.warning(message)
        if log_level == 'error':
            logger.error(message)
    # print("start")
    # delete_unused('logging.log')
    # print("ending")


def delete_unused(filename):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        # str_lines = f'{lines}'
        # caract = ['[', ']']
        # for caract in ['[', ']']:
        #     while caract in str_lines:
        #         str_lines = str_lines.replace(caract, '')
        #         # print('&&',str_lines)

        # # print('lineslineslineslineslineslines',lines)
        # reg = '^\d+/\d+/\d+\s+.+autoreload$'
        # reg2 = 'loggin_mixin.py'
        # ma = re.search(reg2, str_lines, flags=re.IGNORECASE)
        # print(ma)

        for i, line in enumerate(lines):
            reg = '^\d+/\d+/\d+\s+.+autoreload$'
            ma = re.search(reg, f'{lines}')
            rp = re.sub(reg, " ", f'{lines}')
            print('&&', ma)
            print('##', rp)
            # if results:
            #     lines.pop(i)

            # write the result to the file

    # replacements = ''
    # for line in fileinput.input(filename, inplace=True):
    # for search_for in replacements:
    #      replace_with = replacements[search_for]
    #     line = line.replace(search_for, replace_with)
    #     print(line, end='')
    # print(line)
