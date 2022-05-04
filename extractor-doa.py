#coding: utf-8
from operator import ge
import commands
import math

#get files names 
def get_files_names():
    return commands.getoutput("git ls-files").split("\n")#extract files names

#return all author devolopers in repository 
def get_authors_name():
    return commands.getoutput("git log --format='%aN' | sort -u").split('\n')
authors_name = get_authors_name()

# return log commits by author
def calculate_commit_by_author(author):
    return commands.getoutput("git log --name-only --author=\""+author+"\" --pretty=format: | sort | uniq -c | sort -nr").split('\n')

#get list files modify by author 
def get_all_files_changes_by_author(author):
    return commands.getoutput("git log --pretty=\"%H\" --author=\""+author+"\" | while read commit_hash; do git show --oneline --name-only $commit_hash | tail -n+2; done | sort | uniq")

#get list files creating
def get_all_files_creating_by_author(author):
    return commands.getoutput("git log --author=\"" + author + "\" --no-merges --name-status --diff-filter=A --format='> %aN' | awk '/^>/ {tagline=$0} /^A\\t/ {print tagline \"\\t\" $0}'").replace(">","").replace("\t",",").split("\n")

def filter_files_changes_exception(file, files_modified_by_author):
    return list(filter(lambda x: x != file, files_modified_by_author))

#Creating dictonary files and number commits for all author
def creating_dictonary_commits_by_author():
    files_names = get_files_names()
    files_by_commit_by_author = {}
    for file in files_names:
        files_by_commit_by_author.update({file : {}})
    return files_by_commit_by_author    


def calculate_change_all_authors(files_by_commit_by_author):
    for author in authors_name:
        #Recupera a quantidade de commits por author
        logs = calculate_commit_by_author(author)
        if len(logs) > 1 :
            for log in logs:
                log_atual = log.strip().split(" ")
                if len(log_atual) > 1:
                    if log_atual[1] in files_by_commit_by_author.keys():
                        files_by_commit_by_author[log_atual[1]].update({author : int(log_atual[0])})

def calculate_DL_and_AC_other_files(files, author, commits_by_authors, doaa_author):
     for file in files:
        ac  = 0
        if commits_by_authors.get(file) != None: 
           ac  = calculate_AC(author, commits_by_authors.get(file))
           dl  = calculate_DL(author, file)
           doaa_author.update({file: [0, dl, ac]})
            
def calculate_AC(author, changes):
    if changes.get(author) != None:
        return reduce(lambda x, value:x + value, changes.itervalues(), 0) - changes.get(author)
    else:
        return 0

def calculate_DL(author, file):
    dl = 0
    logs = calculate_commit_by_author(author)
    if len(logs) > 1 :
            for log in logs:
                log_atual = log.strip().split(" ")
                if len(log_atual) > 1:
                    if file == log_atual[1]:
                        dl = int(log_atual[0])
    return dl         
              
def calculate_FA(author,commits_by_authors):
    #doaa_authors = {file : (FA,DL,AC)}
    doaa_author = {}
    logs = get_all_files_creating_by_author(author)
    files_modified_all_by_author = get_all_files_changes_by_author(author).split("\n")
    if len(logs) > 1:
        for log in logs:
            log = log.split(',')
            ac  = 0
            if commits_by_authors.get(log[2]) != None: 
               ac  = calculate_AC(author, commits_by_authors.get(log[2]))
            dl  = calculate_DL(author, log[2])
            doaa_author.update({log[2]: [1, dl, ac]})
            
            files_modified_all_by_author = filter_files_changes_exception(log[2],files_modified_all_by_author)
  
    calculate_DL_and_AC_other_files(files_modified_all_by_author, author, commits_by_authors, doaa_author)
    return doaa_author

def calculate_DOAA(author, commits_by_authors):
    return calculate_FA(author, commits_by_authors)

def calculate_doa(fa, dl, ac):
    return 3.293 + (1.098 * fa) + (0.164 * dl) - 0.321 * math.log(1 + ac)

#doa = {author : {file : (FA, DL, AC)}}
doa = {}
def creating_autority_deegree(doa):
    commits_by_authors = creating_dictonary_commits_by_author()
    calculate_change_all_authors(commits_by_authors)
    for author in authors_name:
        doa.update({author : calculate_DOAA(author, commits_by_authors)})

creating_autority_deegree(doa)

dao_files = {}
for k,v in doa.iteritems():
    doa_calculado = {}
    for f, doaa in v.iteritems():
         doa_calculado.update({f : calculate_doa(doaa[0],doaa[1],doaa[2]) })
    dao_files.update({k : doa_calculado })



result_dict = {}
for file in get_files_names():
    result_dict.update({file:[]})

for k,v in dao_files.iteritems():
    print(k)
    for f, doa in v.iteritems():
        print(f,doa)
        if result_dict.get(f) != None:
           result_dict.get(f).append({k : doa})

result_loc = open('result-doa.log','a')
for k,v in result_dict.iteritems(): 
    result_loc.writelines(k +":"+str(v) + '\n')
    print(k, v)   
result_loc.close()

    #commands.getoutput("git log --no-merges --name-status --diff-filter=A --format='> %aN' | awk '/^>/ {tagline=$0} /^A\\t/ {print tagline \"\\t\" $0}'"))

#lista os arquivos criados pelo author
#git log --pretty="%H" --author="authorname" | while read commit_hash; do git show --oneline --name-only $commit_hash | tail -n+2; done | sort | uniq

#Lista a quantidade de arquivos modificados pelo autor
#git log --pretty --author="" --name-only | sort -u | wc -l 
#git log --pretty="%H" --author="authorname" | while read commit_hash; do git show --oneline --name-only $commit_hash | tail -n+2; done | sort | uniq
