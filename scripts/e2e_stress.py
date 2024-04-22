import os
import sys
import glob
from stress_common import *


TEST_COUNT = 5
CLIENT_PORT = 5173
CLIENT_IP = '127.0.0.1'
CLIENT_URL = f"http://{CLIENT_IP}:{CLIENT_PORT}"


def run_test(test_idx: int, thread_id: int = 0) -> int:
    print(f"Running test iteration {test_idx}")
    test_exit_code = os.system('python ./e2e/e2e_main.py')
    if test_exit_code != 0:
        print_err_log(f"[THREAD-{thread_id}] Test iteration {i} faild")
        return 1
    return 0


# check current directory
dir_content = glob.glob('*')
if 'e2e' not in dir_content:
    print_err_log('No E2E tests found in this directory')
    sys.exit(1)


# check client
if not is_port_open(CLIENT_IP, CLIENT_PORT):
    print_err_log(f"Client {CLIENT_URL} is offline")
    sys.exit(1)


# run stress e2e test
for i in range(TEST_COUNT):
    rc = run_test(i)
    if rc != 0:
        print_err_log(f"E2E stress test iteration: {i} faild")
        sys.exit(rc)
print('E2E stress test finished successfully')
