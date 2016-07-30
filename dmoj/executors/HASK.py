from dmoj.executors.base_executor import CompiledExecutor
from dmoj.executors.mixins import NullStdoutMixin


class Executor(NullStdoutMixin, CompiledExecutor):
    ext = '.hs'
    name = 'HASK'
    command = 'ghc'
    command_paths = ['ghc']
    syscalls = ['newselect', 'select']
    test_program = '''\
main = do
    a <- getContents
    putStr a
'''

    def get_compile_args(self):
        return [self.get_command(), '-O', '-o', self.problem, self._code]

    @classmethod
    def get_version_flags(cls, command):
        return ['--version']