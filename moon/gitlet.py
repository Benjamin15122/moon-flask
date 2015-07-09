from moon import *
import subprocess

def git_update_check(path):
    def wrapper(method):
        return GitPathChecker(path, method)

    return wrapper

class GitPathChecker:

    def __init__(self, path, callback):
        self.path = path
        self.callback = callback
        self.path_hash = None

    def update(self, *args, **kwargs):
        new_path_hash = get_path_hash(self.path);

        if self.path_hash != new_path_hash:
            self.path_hash = new_path_hash
            self.value = self.callback(*args, **kwargs)

        return self.value

    def __call__(self, *args, **kwargs):
        ''' shortcut for update
        '''
        return self.update(*args, **kwargs)

#TODO get hash of a single path a time
def get_path_hash(path):
    return subprocess.check_output(GIT_SHOW_HEAD_HASH + [path])
