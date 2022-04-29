# -*- coding: utf-8 -*-
import os
import commands
import csv

relatorio_geral = '../relatorio-geral.csv'
relatorio_projeto = './relatorio.csv'
############################ UTILS ############################
quant_files_validos = 0 
extensoes_permitidas = ['.java','.py','.html','.css','.js','.xml','.c', '.clj', '.cpp', '.sql','.ymal','yml','.sh'];
def verificaEntidadeValida(entidade):
    for extensao in extensoes_permitidas:
        if extensao.lower() in entidade.lower():
            return True
    return False
    

########################## GERA RELATORIOS ########################

def gerar_linha(entidade,m_commit, m_loc, m_doa, convergencia,divergencia):
    return [entidade,m_commit, m_loc, m_doa,convergencia,divergencia]

def criar_linha(nova_linha):
    return nova_linha + '\n'

def save(nomeArquivo, linha):
    f = open(nomeArquivo, "a")         
    f.write(criar_linha(linha))
    f.close()

def get_experts_by_metric(commits_dict):
    return [k for k, v in commits_dict.items() if v == max(commits_dict.values())] # getting all keys containing the `maximum`

#experts_in_files = {file: {[commit(nome_dev), loc(nome_dev), doa(nome_dev)]}}
experts_in_files = {}

#read file names
def extract_files_name():
    experts_in_files = {}
    files_name_log = open('files-name.log','r')
    for file in files_name_log:
        if verificaEntidadeValida(file):
            experts_in_files.update({file.replace('\n',''): []})
    files_name_log.close()
    return experts_in_files

#extract commits logs and calculate maior modificador por arquivo.
def extract_expert_by_commit_metric(experts_in_files):
    commits_log_extract = open('result-commits.log','r')
    for log in commits_log_extract:
        log = log.strip()
        file = log[ 0 : log.index(":")]
        if experts_in_files.get(file)  != None:
            commits = log[log.index("[") : int(log.index("]") + 1)].replace("[","").replace("]","").split(',')
            commits_dict = {}
            for commit in commits:
                metric = commit.replace("{","").replace("}","").replace("\'",'').split(":")
                if len(metric) > 1:
                    commits_dict.update({metric[0].strip(): int(metric[1])})
            
            item  = experts_in_files.get(file)
            if len (commits_dict) >= 1 :   
                item.append(get_experts_by_metric(commits_dict)[0])
            else:
                item.append('S.E.C')

    commits_log_extract.close()

def extract_expert_by_loc_metric(experts_in_files):
    loc_log_extract = open('result-loc.log','r')
    for log in loc_log_extract:
        log = log.strip()
        file = log[ 0 : log.index(":")]
        if experts_in_files.get(file)  != None:
            locs = log[log.index("[") : int(log.index("]") + 1)].replace("[","").replace("]","").split(',')
            loc_dict = {}
            for loc in locs:
                metric = loc.strip().replace("{","").replace("}","").replace("\'",'').split(":")
                if len(metric) > 1:
                    loc_dict.update({metric[0]: int(metric[1])})

            item  = experts_in_files.get(file)
            if len(loc_dict) >= 1:
                item.append(get_experts_by_metric(loc_dict)[0])
            else:
                item.append('S.E.L')

    loc_log_extract.close()

def extract_expert_by_doa_metric(experts_in_files):
    doa_log_extract = open('result-doa.log','r')
    for log in doa_log_extract:
        log = log.strip()
        file = log[ 0 : log.index(":")]
        if experts_in_files.get(file)  != None:
            doas = log[log.index("[") : int(log.index("]") + 1)].replace("[","").replace("]","").split(',')
            doa_dict = {}
            for doa in doas:
                metric = doa.strip().replace("{","").replace("}","").replace("\'",'').split(":")
                if len(metric) > 1:
                    doa_dict.update({metric[0]: float(metric[1])})
            item = experts_in_files.get(file)                
            if len(doa_dict) >=1:
                item.append(get_experts_by_metric(doa_dict)[0])
            else:
                item.append('S.E.D')

    doa_log_extract.close()


#0: [0 experts]
#1: [apenas 1 expert nas 3 métricas] as três métricas indicaram o mesmo cara 
#2: [2 experts iguais nas 3 métricas] duas das três métricas indicaram o mesmo cara
#3: [3 expert  diferentes] cada métrica recomendou um desenvolvedor
# apenas duas métrica foi capaz de encontra um expert %
# apenas duas  % 
#number_expert = [0,0,0,0]

def calculate_experts_by_metrics(experts,number_expert):
    tam = len(experts)
    if tam == 0:
       #Não tem experts pelas 3 métricas(entidades órfas)
       number_expert[0] += 1
    elif(tam == 1):
        #Apenas um expert pelas 3 métricas e apenas um métrica foi capaz de medir 
       number_expert[1] += 1
    #apenas duas métrica que encontraram um expert
    elif(tam == 2):
        #o mesmo expert nas duas métricas 
        if(experts[0] == experts[1]):
           number_expert[1] += 1
        else:
           number_expert[2] += 1   
    elif(tam == 3):
        # 3 métricas calcularam os experts
        if(experts[0] == experts[1] and experts[0] == experts[2]):
            #mesmo experts para 3 métricas
            number_expert[1] += 1
        elif(experts[0] == experts[1] or experts[0] == experts[2] or experts[1] == experts[2]):
            number_expert[2] += 1
        else:
            number_expert[3] += 1

def calcular_percentual (total_entidades, numero_indicacao):
    return (float(numero_indicacao) / float(total_entidades) ) * 100

class Resultado:
    def __init__(self,entidade, esp_dev_commit, esp_dev_loc, esp_dev_doa, conv_3_2, conv_3_3, div):
       self.entidade = entidade
       self.esp_dev_commit = esp_dev_commit
       self.esp_dev_loc = esp_dev_loc
       self.esp_dev_doa = esp_dev_doa
       self.conv_3_2 = conv_3_2
       self.conv_3_3 = conv_3_3
       self.div = div
    
    def __str__(self):
            return self.entidade + "," + self.esp_dev_commit + "," + self.esp_dev_loc + "," + self.esp_dev_doa + "," + self.conv_3_2 + "," + self.conv_3_3 + "," + self.div 
            
    def getConv_3_2(self):
        return self.conv_3_2;
        
    def getConv_3_3(self):
        return self.conv_3_3;

    def getDiv(self):
        return self.div;

def setEntidade(entidade):
     if "/" in entidade:
        return entidade[entidade.rindex("/")+1:len(entidade)]
     else: 
        return entidade
        
def gerar_experts(experts_in_files):
    #resultado = {file,esp_dev_commit,esp_dev_loc,esp_dev_doa,conv_3_2,conv_3_3,div}
    resultados = []
    for k,v in experts_in_files.iteritems():      
        number_expert = [0,0,0,0]
        calculate_experts_by_metrics(v,number_expert)

        entidade = k
        esp_dev_commit = v[0]
        esp_dev_loc = v[1]
        esp_dev_doa = v[2]
        conv_3_2 = ("X" if number_expert[2] == 1 else "O")
        conv_3_3 = ("X" if number_expert[1] == 1 else "O")
        div = ("X" if number_expert[3] == 1 else "O")
        
        resultados.append(Resultado(setEntidade(str(entidade)), esp_dev_commit, esp_dev_loc, esp_dev_doa, conv_3_2, conv_3_3, div))

    return resultados


#################################################
experts_in_files = extract_files_name()

extract_expert_by_commit_metric(experts_in_files)
extract_expert_by_loc_metric(experts_in_files)
extract_expert_by_doa_metric(experts_in_files)


resultado = gerar_experts(experts_in_files)
save(relatorio_geral,'Entidade,Métrica commit,Métrica LOC,Métrica DOA,Convergência de 2 para 3,Convergência de 3 para 3,Divergência')
save(relatorio_projeto,'Entidade,Métrica commit,Métrica LOC,Métrica DOA,Convergência de 2 para 3,Convergência de 3 para 3,Divergência')

#totalizadores
total_conv_3_2 = 0
total_conv_3_3 = 0
total_divergencia = 0
total_sem_indicacao = 0
for k in resultado:      
    if k.getConv_3_2() == 'X':
        total_conv_3_2 = total_conv_3_2 + 1
    
    if k.getConv_3_3() == 'X':
        total_conv_3_3 = total_conv_3_3 + 1
    
    if k.getDiv() == 'X':
        total_divergencia = total_divergencia + 1
    
        
    print(k)
    save(relatorio_projeto, str(k))
    save(relatorio_geral, str(k))
print ('+---------------------------------------+')
name = str(commands.getoutput("git remote -v | cut -f2").split(" ")[0])
name = name[name.rfind("/")+1:name.rfind(".")]
print(name)

total_files = int(commands.getoutput("git ls-files | wc -l"))
print('Total Files: ' + str(total_files))
print('\n')
print('Total de entidades consideradas:',len(experts_in_files))
print('Total de convergência de 3 x 3: ',total_conv_3_3)
print('Total de convergência de 3 x 2',total_conv_3_2)
print('Total de divergência',total_divergencia)

save('../estatiscas-projetos.csv','Projeto,Total de Entidades,Total de Entidades Consideradas')
save('../estatiscas-projetos.csv',name+','+str(total_files)+','+str(len(experts_in_files)))
# sem_expert     = calcular_percentual(total_files,number_expert[0])
# convergencia   = calcular_percentual(total_files,number_expert[1])
# divergencia    = calcular_percentual(total_files,number_expert[2])