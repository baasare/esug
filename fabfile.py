import os

from fabric.api import local

EXCLUDED_LIBRARIES = [
    "pywin32",
    "pywin32-ctypes",
    "pywinpty"
]


def delete_line_by_full_match(original_file, line_to_delete):
    """ In a file, delete the lines at line number in given list"""
    is_skipped = False
    dummy_file = original_file + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            line_to_match = line
            if line[-1] == '\n':
                line_to_match = line[:-1]
            # if current line matches with the given line then skip that line
            if line_to_delete not in line_to_match:
                write_obj.write(line)
            else:
                is_skipped = True

    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)


def deploy():
    local('pip freeze > requirements.txt')

    for lib in EXCLUDED_LIBRARIES:
        delete_line_by_full_match("requirements.txt", lib)

    local('git add .')
    print("enter your git commit comment: ")
    comment = input()
    local('git commit -m "%s"' % comment)
    local('git push -u origin master')
    # local('heroku maintenance:on --app usug')
    # local('heroku maintenance:off --app usug')
    # local('heroku logs --tail --app usug')
