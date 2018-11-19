
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
WRITE_UPDATE = 'write_update'
COPY = 'copy'

BUS_UPDATE = "bus_update"
BUS_READ = "bus_read"
MEM_READ = 'mem_read'
INVALIDATE = 'invalidate'
RWITM = 'rwitm' #Read with Intent to Modify

MODIFIED = 'modified'
EXCLUSIVE = 'exclusive'
SHARED = 'shared'
SHARED_CLEAN = "shared_clean"
SHARED_MODIFIED = "shared_modified"
INVALID = 'invalid'


MESI_STATE_MACHINE = {
    INVALID: {
        READ: (EXCLUSIVE, MEM_READ, 100),
        COPY: (SHARED, MEM_READ, 100),
        WRITE: (MODIFIED, RWITM, 100),
        MEM_READ: (INVALID, None, 0),
        RWITM: (INVALID, None, 0)
    },
    SHARED: {
        READ: (SHARED, None, 0),
        WRITE: (MODIFIED, RWITM, 0),
        MEM_READ: (SHARED, None, 0),
        RWITM: (INVALID, None, 0)
    },
    MODIFIED: {
        READ: (MODIFIED, None, 0),
        WRITE: (MODIFIED, None, 0),
        MEM_READ: (SHARED, None, 100),
        RWITM: (INVALID, None, 100)
    },
    EXCLUSIVE: {
        READ: (EXCLUSIVE, None, 0),
        WRITE: (MODIFIED, None, 0),
        MEM_READ: (SHARED, None, 0),
        RWITM: (INVALID, None, 0)
    }
}

DRAGON_STATE_MACHINE = {
    INVALID: {
        COPY: (SHARED_CLEAN, BUS_READ, 0),
        READ: (EXCLUSIVE, BUS_READ, 100),
        WRITE: (MODIFIED, BUS_READ, 100),
        WRITE_UPDATE: (SHARED_MODIFIED, BUS_UPDATE, 0),
    },
    SHARED_CLEAN: {
        READ: (SHARED_CLEAN, None, 0),
        WRITE: (MODIFIED, None, 0),
        WRITE_UPDATE: (SHARED_MODIFIED, BUS_UPDATE, 0),
        BUS_READ: (SHARED_CLEAN, None, 0),
        BUS_UPDATE: (SHARED_CLEAN, None, 0)
    },
    SHARED_MODIFIED: {
        READ: (SHARED_MODIFIED, None, 0),
        WRITE: (MODIFIED, None, 0),
        WRITE_UPDATE: (SHARED_MODIFIED, BUS_UPDATE, 0),
        BUS_READ: (SHARED_MODIFIED, None, 0),
        BUS_UPDATE: (SHARED_CLEAN, None, 0)
    },
    MODIFIED: {
        READ: (MODIFIED, None, 0),
        WRITE: (MODIFIED, None, 0),
        BUS_READ: (SHARED_MODIFIED, None, 0)
    },
    EXCLUSIVE: {
        READ: (EXCLUSIVE, None, 0),
        WRITE: (MODIFIED, None, 0),
        BUS_READ: (SHARED_CLEAN, None, 0)
    }
}


