import os
import commands

#get files names 
def get_files_names():
    return commands.getoutput("git ls-files").split("\n") #extract files names

result_commits_log = open('files-name.log','a')
for line in get_files_names():
     result_commits_log.writelines(line + '\n')