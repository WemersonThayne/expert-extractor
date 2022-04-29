import os
import commands

total_devs = commands.getoutput("git shortlog -s -n --all | wc -l")
def extrarctor_commits_by_all_author():
    
    
    print ('+---------------------------------------+')
    print ('|      TOTAL OF COMMITS BY AUTHOR       |')
    print ('+---------------------------------------+')

    total_commits_by_authors = commands.getoutput("git shortlog -s -n --all").split("\n")
    total_devs = len(total_commits_by_authors)
    commits_by_author = {}

    for commits_author in total_commits_by_authors:
        split_commit = commits_author.split("\t")
        commits_by_author.update({split_commit[1]: split_commit[0].strip()})
        print(split_commit[1]+":"+split_commit[0])
    return commits_by_author

#get files names 
def get_files_names():
    return commands.getoutput("git ls-files").split("\n")#extract files names

#Creating dictonary files and number commits for all author
def creating_dictonary_commits_by_author():
    files_names = get_files_names()
    files_by_commit_by_author = {}
    for file in files_names:
        files_by_commit_by_author.update({file : []})
    return files_by_commit_by_author    


def get_authors_name():
    #return all author devolopers in repository 
    return commands.getoutput("git log --format='%aN' | sort -u").split('\n')

def get_locs_by_author(author):
    locs_by_authors = {}
    locs_by_author_log = commands.getoutput("git log --author=\""+author+"\" --no-merges  --pretty=tformat:\"%aN\" --numstat")
    locs_by_author_log = locs_by_author_log.strip().replace("\t",",").replace(author,"").split("\n")


    for loc in locs_by_author_log:
        if loc != "" :
            log_array = loc.split(",")
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


def calculate_commit_by_author(author):
    return commands.getoutput("git log --name-only --author=\""+author+"\" --pretty=format: | sort | uniq -c | sort -nr").split('\n')

def calculate_loc_by_author_files(author):
    return commands.getoutput("git log --author=\""+author+"\" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf \"added lines: %d, removed lines: %d, total lines: %d\\n\", add, subs, loc }' -")

def calculate_change(authors, total_commits_by_authors, total_lines_by_author_in_file, files_by_commit_by_author):
    for author in authors:
        #Recupera a quantidade de commits por author
        logs = calculate_commit_by_author(author)
        total_lines_by_author.update({author : calculate_loc_by_author_files(author)})
        total_lines_by_author_in_file.update({author: get_locs_by_author(author)})

        if len(logs) > 1 :

            for log in logs:
                log_atual = log.strip().split(" ")
                if len(log_atual) > 1:
                    if log_atual[1] in files_by_commit_by_author.keys():
                        item = files_by_commit_by_author.get(log_atual[1])
                        files_by_commit_by_author[log_atual[1]].append({author : log_atual[0]})


############### functions ######################
print ('+---------------------------------------+')
name = commands.getoutput("git remote -v").split("\n")[0]
name = name.split("\t")[1]
name = name.split(" ")[0]
print(name)

commits_total  = commands.getoutput("git rev-list --all --count")
print('Total Commits: ' + commits_total)

total_files = commands.getoutput("git ls-files | wc -l")
print('Total Files: ' + total_files)

total_lines_changed = commands.getoutput("git log --numstat --format=\"\" \"$@\" | awk '{files += 1}{ins += $1}{del += $2} END{print \" \"ins\" insertions(+) \"del\" deletions(-)\"}'")
print('Total Lines Changed: ' + total_lines_changed)

print('Total Devs:' + total_devs)
print ('+---------------------------------------+')

print('\n')

extrarctor_commits_by_all_author()

print ('+---------------------------------------+')


#Get dictornaty author and commits
commits_by_author  = creating_dictonary_commits_by_author()

#Get names authors of commits
authors_logs = get_authors_name()

#Total lines change by author general
total_lines_by_author = {}

#Total lines changes by author on each files
total_lines_by_author_in_file = {}

calculate_change(authors_logs, total_lines_by_author,total_lines_by_author_in_file, commits_by_author)

print('\n')
print('+----------- Total commits by authors each files ---------------+')
result_commits_file = open('result-commits.log','a')
for k,v in commits_by_author.iteritems(): 
    result_commits_file.writelines(k +":"+str(v) + '\n')
    print(k, v)   
result_commits_file.close()

print('\n')
print('+----------- Total lines changed all authors ---------------+')
for k,v in total_lines_by_author.iteritems(): 
    print(k, v)   
print ('+---------------------------------------+')

print('\n')
print('+----------- Total lines changed all authors ---------------+')
result_dict = {}
for file in get_files_names():
    result_dict.update({file:[]})


for k,v in total_lines_by_author_in_file.iteritems():   
    for file, value in v.iteritems():   
        value = tuple(value)
        if result_dict.get(file) != None:
           result_dict.get(file).append({k : (value[0] - value[1])})
print ('+---------------------------------------+')


result_loc = open('result-loc.log','a')
for k,v in result_dict.iteritems(): 
    result_loc.writelines(k +":"+str(v) + '\n')
    print(k, v)   
result_loc.close()


