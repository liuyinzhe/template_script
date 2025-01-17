from pathlib import Path
from Bio import SeqIO

def GetAllFilePaths(pwd,wildcard='*'):
    '''
    获取目录下文件全路径，通配符检索特定文件名，返回列表
    param: str  "pwd"
    return:dirname pathlab_obj
    return:list [ str ]
    #https://zhuanlan.zhihu.com/p/36711862
    #https://www.cnblogs.com/sigai/p/8074329.html
    '''
    files_lst = []
    target_path=Path(pwd)
    for child in target_path.rglob(wildcard):
        if child.is_symlink():
            pass
        elif child.is_dir():
            pass
        elif child.is_file():
            files_lst.append(child)
    return files_lst

def  parse_gb2fasta(gb_path):
    # 提取完整序列并格式为 fasta
    gb_record = SeqIO.read(gb_path, "genbank")
    '''
        ID: PQ289630.1
        Name: PQ289630
        Description: Getah virus isolate GETV-QJ, complete genome
        Number of features: 3
        /molecule_type=ss-RNA
        /topology=linear
        /data_file_division=VRL
        /date=16-OCT-2024
        /accessions=['PQ289630']
        /sequence_version=1
        /keywords=['']
        /source=Getah virus (GETV)
        /organism=Getah virus
        /taxonomy=['Viruses', 'Riboviria', 'Orthornavirae', 'Kitrinoviricota', 'Alsuviricetes', 'Martellivirales', 'Togaviridae', 'Alphavirus']
        /references=[Reference(title='Direct Submission', ...)]
        /structured_comment=defaultdict(<class 'dict'>, {'Assembly-Data': {'Sequencing Technology': 'Sanger dideoxy sequencing'}})
        Seq('ATGGCGGACGTGTGACATCACCGTTCGCTCTTTCTAGGATCCTTTGCTACTCCA...TAC')
    '''
    seq_id = gb_record.id
    complete_seq = str(gb_record.seq)
    complete_seq_str = ">"+seq_id+"\n"+complete_seq
    description = gb_record.description
    taxonomy_list = gb_record.annotations['taxonomy'] # ['Viruses', 'Riboviria', 'Orthornavirae', 'Kitrinoviricota', 'Alsuviricetes', 'Martellivirales', 'Togaviridae', 'Alphavirus']
    accessions = gb_record.annotations['accessions'][0] # ['NC_006558']
    source = gb_record.annotations['source'] # 'source': 'Getah virus (GETV)'
    organism = gb_record.annotations['organism'] #'organism': 'Getah virus'
    topology = gb_record.annotations['topology'] # linear
    molecule_type = gb_record.annotations['molecule_type'] # ss-RNA
    dbxrefs_lst = gb_record.dbxrefs # []
    
    cds_num = 1
    for feature in gb_record.features:
        cds_name = ""
        cds_seq = ""
        translation_seq = ""
        if feature.type == "CDS":
            cds_name = ">" + seq_id + "_cds_" + \
                    feature.qualifiers['protein_id'][0] + \
                    "_" + str(cds_num) + \
                    " [protein=" + feature.qualifiers['product'][0] + "]" + \
                    " [protein_id=" + feature.qualifiers['protein_id'][0] + "]" + " [gbkey=CDS]"
            cds_num += 1
            translation_seq = feature.qualifiers['translation'][0]

        for item in feature.location.parts:
            cds_seq += complete_seq[item.start:item.end]
        out_cds_fasta_str = cds_name+"\n"+cds_seq
        out_translation_fasta_str = cds_name+"\n"+translation_seq

        #print(out_cds_fasta_str)
        #feature_location = feature.location
        #print(cds_num,feature_location.parts)
        #print(feature.qualifiers)
        '''
        type: CDS
        location: [7526:11288](+)
        qualifiers:{'note': ['C-E3-E2-6K-E1'], 
        'codon_start': ['1'], 
        'product': ['structural polyprotein'], 
        'protein_id': ['XHY85262.1'], 
        'translation': ['MNYIPTQTFYGRRWRPRPAYRPWRVPMQPAPPMVIPELQTPIVQAQQMQQLISAVSALTTKQNGKAPKKPKKKPQKAKAKKNEQQKKNENKKPPPKQRNPAKKKKPGKRERMCMKIENDCIFEVKLDGKVTGYACLVGDKVMKPAHVKGVIDNPDLAKLTYKKSSKYDLECAQIPVHMKSDASKYTHEKPEGHYNWHHGAVQYSGGRFTIPTGAGKPGDSGRPIFDNKGRVVAIVLGGANEGARTALSVVTWTKDMVTRYTPEGTEEWSAALMMCVLANVTFPCSEPACAPCCYEKQPEQTLRMLEDNVDRPGYYDLLEATMTCNNSARHRRSVTEHFNVYKATKPYLAYCADCGDGQFCYSPVAIEKIRDEASDGMIKIQVAAQIGINKGGTHEHNKIRYIAGHDMKEANRDSLQVHTSGVCAIRGTMGHFIVAYCPPGDELKVQFQDAESHTQACKVQYKHAPAPVGREKFTVRPHFGIEVPCTTYQLTTAPTEEEIDMHTPPDIPDITLLSQQSGNVKITAGGKTIRYNCTCGSGNVGTTSSDKTINSCKIAQCHAAVTNHDKWQYTSSFVPRADQLSRKGKVHVPFPLTNSTCRVPVARAPGVTYGKRELTVKLHPDHPTLLTYRSLGADPRPYEEWIDRYVERTIPVTEEGIEYRWGNNPPVRLWAQLTTEGKPHGWPHEIILYYYGLYPAATIAAVSAAGLAVVLSLLASCYMFATARRKCLTPYALTPGAVVPVTLGVLCCAPRAHAASFAESMAYLWDENQTLFWLELATPLAAIIILVCCLKNLLCCCKPLSFLVLVSLGTPVVKSYEHTATIPNVVGFPYKAHIERNGFSPMTLQLEVLGTSLEPTLNLEYITCEYKTVVPSPYIKCCGTSECRSMERPDYQCQVYTGVYPFMWGGAYCFCDTENTQLSEAYVDRSDVCKHDHAAAYKAHTAAMKATIRISYGNLNQTTTAFVNGEHTVTVGGSRFTFGPISTAWTPFDNKIVVYKNDVYNQDFPPYGSGQPGRFGDIQSRTVESKDLYANTALKLSRPSSGTVHVPYTQTPSGFKYWIKERGTSLNDKAPFGCVIKTNPVRAENCAVGNIPVSMDIPDTAFTRVIDAPAVTNLECQVAVCTHSSDFGGIATLTFKTDKPGKCAVHSHSNVATIQEAAVDIKTDGKITLHFSTASASPAFKVSVCSAKTTCMAACEPPKDHIVPYGASHNNQVFPDMSGTAMTWVQRVAGGLGGLTLAAVAVLILVTCVTMRR']
        }
        '''
    return complete_seq_str,out_cds_fasta_str,out_translation_fasta_str
            

def main():
    # script_path =Path(__file__)
    # script_dir = Path(script_path).parent
    # print(script_dir)
    current_path = Path.cwd()
    out_dir = current_path.joinpath('out')
    all_gb_lst = GetAllFilePaths(current_path,'*.gb')
    for gb_path in all_gb_lst:
        file_name = gb_path.stem
        print(gb_path.stem)
        sample_dir = out_dir.joinpath(file_name)
        sample_dir.mkdir(exist_ok=True,parents=True)
        cds_fasta_path = sample_dir.joinpath('cds.fasta')
        protein_fasta_path = sample_dir.joinpath('protein.fasta')
        complete_fasta_path = sample_dir.joinpath('complete.fasta')
        complete_seq_str,cds_fasta_str,translation_fasta_str = parse_gb2fasta(gb_path)
        with open(complete_fasta_path,mode='wt',encoding='utf-8') as f:
            f.write(complete_seq_str+'\n')
        
        with open(cds_fasta_path,mode='wt',encoding='utf-8') as f:
            f.write(cds_fasta_str+'\n')
            
        with open(protein_fasta_path,mode='wt',encoding='utf-8') as f:
            f.write(translation_fasta_str+'\n')

if __name__ == '__main__':
    main()