import datetime
import glob
import os
import shutil
import signal
import subprocess
import sys
import time
from typing import List

from baserunner import Runner, main


class MacRunner(Runner):
    """
    Mac runner
    """

    def __init__(self, path: str, args: List[str], **kwargs):
        super().__init__(path, args, **kwargs)

        self.lldb_path = shutil.which('lldb')
        if not self.lldb_path:
            raise Exception('Could not find lldb')

    @classmethod
    def get_dump_dir(cls) -> str:
        return '/cores'

    @classmethod
    def get_dump_pattern(cls) -> str:
        """
        Get file pattern to find dump files
        """
        return "core.*"

    @classmethod
    def install(cls):
        # This is equal to "ulimit -c unlimited"
        import resource
        val1, val2 = resource.getrlimit(resource.RLIMIT_CORE)
        if val1!=resource.RLIM_INFINITY or val2!=resource.RLIM_INFINITY:
            cls.info('Setting ulimit -c..')
            resource.setrlimit(resource.RLIMIT_CORE,
                            (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

        # Find lldb
        errors = []
        lldb_path = shutil.which('lldb')
        if not lldb_path:
            errors.append('Could not find lldb')

        if errors:
            cls.err('ERROR: ' + ' '.join(errors))
            sys.exit(1)
        
        cls.info('Running infrastructure is ready')
        #os.system('echo "ulimit -c    : `ulimit -c`"')

    def warmup(self):
        """
        This will be called before run()
        """
        self.install()

    def get_dump_path(self) -> str:
        dump_dir = self.get_dump_dir()
        dump_file = f'core.{self.popen.pid}'
        return os.path.join(dump_dir, dump_file)
        
    def terminate(self):
        """
        Terminate a process and generate dump file
        """
        
        time.sleep(1)
        os.kill(self.popen.pid, signal.SIGQUIT)            

    def process_crash(self):
        """
        Process dump file.
        """
        cmd = f'''{self.lldb_path} --core {self.get_dump_path()} ''' + \
              f'''-o 'bt all' -o quit ''' + \
              f'''{self.path}'''
        self.info(cmd)
        os.system(cmd)


if __name__ == '__main__':
    main(MacRunner)
