#coding: utf-8
import commands 

print("#####################################################")
print("########### EXTRATOR DA MÉTRICA COMMIT ##############")
total_devs = commands.getoutput("git shortlog -s -n --all | wc -l")
def extrarctor_commits_by_all_author():
    
    
    print ('+---------------------------------------+')
    print ('|      TOTAL OF COMMITS BY AUTHOR       |')
    print ('+---------------------------------------+')

    total_commits_by_authors = commands.getoutput("git shortlog -s -n --all").split("\n")
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

def calculate_commit_by_author(author):
    return commands.getoutput("git log --no-merges --name-only --author=\""+author+"\" --pretty=format: | sort | uniq -c | sort -nr").split('\n')

def calculate_change(authors, files_by_commit_by_author):
    for author in authors:
        #Recupera a quantidade de commits por author
        logs = calculate_commit_by_author(author)
        if len(logs) > 1 :
            for log in logs:
                log_atual = log.strip().split(" ")
                if len(log_atual) > 1:
                    if log_atual[1] in files_by_commit_by_author.keys():
                        files_by_commit_by_author[log_atual[1]].append({author : log_atual[0]})

##############################################
print('Iniciondo o processo.....')
print ('+---------------------------------------+')
name = commands.getoutput("git remote -v").split("\n")[0]
name = name.split("\t")[1]
name = name.split(" ")[0]
print(name)

commits_total  = commands.getoutput("git rev-list --all --count")
print('Total Commits: ' + commits_total)

total_files = commands.getoutput("git ls-files | wc -l")
print('Total Files: ' + total_files)

print('Total Devs:' + total_devs)
print ('+---------------------------------------+')

print('\n')

extrarctor_commits_by_all_author()

print ('+---------------------------------------+')


#Get dictornaty author and commits
commits_by_author  = creating_dictonary_commits_by_author()

#Get names authors of commits
authors_logs = get_authors_name()


calculate_change(authors_logs, commits_by_author)
print('\n')
print('+----------- Total commits by authors each files ---------------+')
result_commits_file = open('result-commits.log','a')
for k,v in commits_by_author.iteritems(): 
    result_commits_file.writelines(k +":"+str(v) + '\n')
    print(k, v)   
result_commits_file.close()