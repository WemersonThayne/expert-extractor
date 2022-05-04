

def get_authors_name():
    #return all author devolopers in repository 
    return commands.getoutput("git log --format='%aN' | sort -u").split('\n')