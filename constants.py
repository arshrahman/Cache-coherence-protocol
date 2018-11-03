
FILE_PATH = './data'
FILE_EXTENSION = '.data'
DIRECTORY_EXTENSION = '_four'

MESI = 'mesi'
DRAGON = 'dragon'
WRONG_COMMAND = 'wrong protocol command!'
TOTAL_CORES = 4

LOAD = 0
STORE = 1
OTHER_INSTRUCTION = 2
COUNT = 3

INSTRUCTION_MAP = {0: LOAD, 1: STORE}

READ = 'read'
WRITE = 'write'
COPY = 'copy'


MEM_READ = 'mem_read'
INVALIDATE = 'invalidate'
RWITM = 'rwitm' #Read with Intent to Modify

MODIFIED = 'modified'
EXCLUSIVE = 'exclusive'
SHARED = 'shared'
INVALID = 'invalid'


MESI_STATE_MACHINE = {
    INVALID: {
        READ: (EXCLUSIVE, MEM_READ, 100),
        COPY: (SHARED, MEM_READ, 0),
        WRITE: (MODIFIED, RWITM, 100)
    },
    SHARED: {
        READ: (SHARED, None, 0),
        WRITE: (MODIFIED, INVALIDATE, 0),
        LOAD: (SHARED, MEM_READ, 0),
        STORE: (INVALID, INVALIDATE, 0)
    },
    MODIFIED: {
        READ: (MODIFIED, None, 0),
        WRITE: (MODIFIED, None, 0),
        LOAD: (SHARED, MEM_READ, 100),
        STORE: (INVALID, INVALIDATE, 100)
    },
    EXCLUSIVE: {
        READ: (EXCLUSIVE, None, 0),
        WRITE: (MODIFIED, None, 0),
        LOAD: (SHARED, MEM_READ, 0),
        STORE: (INVALID, RWITM, 0)
    }
}


