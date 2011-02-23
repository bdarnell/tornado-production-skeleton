import os
import site
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))

prev_sys_path = list(sys.path)

# site.addsitedir adds this directory to sys.path then scans for .pth files
# and adds them to the path too.
site.addsitedir(os.path.join(base_dir, 'third_party'))

# addsitedir adds its directories at the end, but we want our local stuff
# to take precedence over system-installed packages.
# See http://code.google.com/p/modwsgi/issues/detail?id=112
new_sys_path = []
for item in list(sys.path):
  if item not in prev_sys_path:
    new_sys_path.append(item)
    sys.path.remove(item)
sys.path[:0] = new_sys_path
