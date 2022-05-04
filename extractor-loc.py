#coding: utf-8
import commands

print("##################################################")
print("########### EXTRATOR DA MÉTRICA LoC ##############")
#get files names 
def get_files_names():
    return commands.getoutput("git ls-files").split("\n")#extract files names

def get_authors_name():
    #return all author devolopers in repository 
    return commands.getoutput("git log --format='%aN' | sort -u").split('\n')

def get_locs_by_author(author):
    locs_by_authors = {}
    locs_by_author_log = commands.getoutput("git log --author=\""+author+"\" --no-merges  --pretty=tformat:\"%aN\" --numstat")
    locs_by_author_log = locs_by_author_log.strip().replace("\t",",").replace(author,"").split("\n")
    print('> Author:', author )
    for loc in locs_by_author_log:
        if loc != "" :
            log_array = loc.split(",")
            print(log_array)
            if len(log_array) >= 3 :    
                add = (log_array[0] != '-' and int(log_array[0]) or 0)
                rem = (log_array[1] != '-' and int(log_array[1]) or 0)
                if log_array[2] in locs_by_authors.keys():            
                     item  = list(locs_by_authors.get(log_array[2]))
                     item[0] += add
                     item[1] += rem
                     locs_by_authors[log_array[2]] = tuple(item)
                else:
                    locs_by_authors.update({log_array[2]:(add, rem)})
    
    return locs_by_authors


def calculate_loc_by_author_files(author):
    return commands.getoutput("git log --author=\""+author+"\" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf \"added lines: %d, removed lines: %d, total lines: %d\\n\", add, subs, loc }' -")

def calculate_change(authors, total_lines_by_author_in_file):
    for author in authors:
        total_lines_by_author.update({author : calculate_loc_by_author_files(author)})
        total_lines_by_author_in_file.update({author: get_locs_by_author(author)})


############### functions ######################
print('Iniciondo o processo.....')
print ('+---------------------------------------+')
name = commands.getoutput("git remote -v").split("\n")[0]
name = name.split("\t")[1]
name = name.split(" ")[0]
print(name)

total_files = commands.getoutput("git ls-files | wc -l")
print('Total Files: ' + total_files)

total_lines_changed = commands.getoutput("git log --numstat --format=\"\" \"$@\" | awk '{files += 1}{ins += $1}{del += $2} END{print \" \"ins\" insertions(+) \"del\" deletions(-)\"}'")
print('Total Lines Changed: ' + total_lines_changed)

print ('+---------------------------------------+')

#Get names authors of commits
authors_logs = get_authors_name()

#Total lines change by author general
total_lines_by_author = {}

#Total lines changes by author on each files
total_lines_by_author_in_file = {}

calculate_change(authors_logs, total_lines_by_author_in_file)

print('\n')
print('+----------- Total lines changed all authors ---------------+')

for k,v in total_lines_by_author.iteritems(): 
    print(k, v)   
print ('+---------------------------------------+')
print('\n')

result_dict = {}
for file in get_files_names():
    result_dict.update({file:[]})

for k,v in total_lines_by_author_in_file.iteritems():   
    for file, value in v.iteritems():   
        value = tuple(value)
        if result_dict.get(file) != None:
           result_dict.get(file).append({k : (value[0] - value[1])})

result_loc = open('result-loc.log','a')
for k,v in result_dict.iteritems(): 
    result_loc.writelines(k +":"+str(v) + '\n')

result_loc.close()