import datetime
import glob
import os
import shutil
import signal
import subprocess
import sys
import time
from typing import List

from runner import Runner, main

# gdb -return-child-result -batch -ex "run" -ex "thread apply all bt" -ex "quit" --args ./${file}

class LinuxRunner(Runner):
    """
    Linux runner
    """

    def __init__(self, path: str, args: List[str], 
                 timeout: int = Runner.TIMEOUT):
        super().__init__(path, args, timeout=timeout)

        self.gdb_path = shutil.which('gdb')
        if not self.gdb_path:
            raise Exception('Could not find gdb')

    @classmethod
    def get_dump_dir(cls) -> str:
        return os.getcwd()

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

        # Set core pattern
        with open('/proc/sys/kernel/core_pattern', 'rt') as f:
            core_pat = f.read()
            core_pat = core_pat.strip()

        if core_pat != 'core':
            cls.info('Setting core_pattern..')
            with open('/proc/sys/kernel/core_pattern', 'wt') as f:
                f.write('core')

        # Find gdb
        errors = []
        gdb_path = shutil.which('gdb')
        if not gdb_path:
            errors.append('Could not find gdb')

        if errors:
            cls.err('ERROR: ' + ' '.join(errors))
            sys.exit(1)
        
        cls.info('Running infrastructure is ready')
        #os.system('echo "ulimit -c    : `ulimit -c`"')
        #os.system('echo "core_pattern : `cat /proc/sys/kernel/core_pattern`"')

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
        
        # Generate core dump for the process
        #os.system(f'sudo gcore {self.popen.pid}')
        
        # We can now terminate the process
        time.sleep(1)
        os.kill(self.popen.pid, signal.SIGQUIT)            


    def process_crash(self):
        """
        Process dump file.
        """
        cmd = f'''{self.gdb_path} -q {self.path} {self.get_dump_path()} ''' + \
              f'''-ex 'set pagination off' ''' + \
              f'''-ex 'set trace-commands on' -ex where -ex 'thread apply all bt' -ex quit'''
        os.system(cmd)



if __name__ == '__main__':
    main(LinuxRunner)
