import os
import appdirs

DIR = appdirs.user_data_dir('dooit')
filename = os.path.join(DIR, "todo.yaml") 