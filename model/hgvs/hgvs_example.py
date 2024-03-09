import hgvs.parser
import hgvs.validator
import hgvs.projector # Automated liftover transcript via common reference.
from hgvs.exceptions import HGVSError
import hgvs.dataproviders.uta
from hgvs.assemblymapper import AssemblyMapper


# Ref:
# https://github.com/biocommons/hgvs/tree/main/examples
# https://hgvs.readthedocs.io/en/stable/

def hgvs2gp(CodingDNA,genome):
    hp = hgvs.parser.Parser()
    if isinstance(CodingDNA, str):
        var_coding_DNA = hp.parse_hgvs_variant(CodingDNA)
    else:
        var_coding_DNA = CodingDNA
    var_genomic_DNA = genome.c_to_g(var_coding_DNA)
    var_protein = genome.c_to_p(var_coding_DNA)
    return var_genomic_DNA,var_protein

def parse_gDNA(var_genomic_DNA,Reference_name_dic):
    '''
    
    NC_000017.10:g.41245466G>A
    NC_000017.10:g.41245466_41245466G>A
    NC_000013.10:g.32907388_32907391del
    NC_000013.10:g.32914865dup
    '''
    #print(type(var_genomic_DNA))#<class 'hgvs.sequencevariant.SequenceVariant'>
    record = re.split(r':g.',str(var_genomic_DNA))
    chrom_id = Reference_name_dic[record[0]]
    if r"_" in record[1]:
        match_obj = re.search(r'(\d+)_(\d+)',record[1])
        start = int(match_obj.group(1))
        end = int(match_obj.group(2))
    else:
        match_obj = re.search(r'(\d+)',record[1])
        start = int(match_obj.group(1))
        end = start
    return chrom_id,start,end

def Normalizing_Genomic_Variation(hgvs_dataprovider_normalized,Any_Variation):
    '''
    Normalizing variants
    In hgvs, normalization means shifting variants 3' (as requried by the HGVS nomenclature) as well as 
    rewriting variants. The variant "NM_001166478.1:c.30_31insT" is in a poly-T run (on the transcript).
    It should be shifted 3' and is better written as dup, as shown below:

                                          *                       NC_000006.11:g.49917127dupA
    NC_000006.11 g   49917117 > AGAAAGAAAAATAAAACAAAG  > 49917137 
    NC_000006.11 g   49917117 < TCTTTCTTTTTATTTTGTTTC  < 49917137 
                                |||||||||||||||||||||  21= 
    NM_001166478.1 n       41 < TCTTTCTTTTTATTTTGTTTC  <       21 NM_001166478.1:n.35dupT
    NM_001166478.1 c       41 <                        <       21 NM_001166478.1:c.30_31insT

    import hgvs.normalizer
    hn = hgvs.normalizer.Normalizer(hdp)
    v = hp.parse_hgvs_variant("NM_001166478.1:c.30_31insT")
    str(hn.normalize(v))

    'NM_001166478.1:c.35dupT'
    '''
    return str(hgvs_dataprovider_normalized.normalize(Any_Variation))

def test():
    print(hgvs.__version__)
    # You only need to do this once per process
    import hgvs.parser
    hgvsparser = hgvs.parser.Parser()

    var_c1 = hgvsparser.parse_hgvs_variant('NM_000059.3:c.7806-14T>C')
    print(var_c1)
    print(var_c1.posedit.pos.start)

    hdp = hgvs.dataproviders.uta.connect()
    am37 = AssemblyMapper(
        hdp, assembly_name='GRCh37', alt_aln_method='splign')# GRCh37,GRCh38 ;alt_aln_method='splign';alt_aln_method='blat'
    var_g = am37.c_to_g(var_c1)
    print(var_g)
    print(am37.relevant_transcripts(var_g))
    #https://github.com/biocommons/hgvs/issues/629

    var_p = am37.c_to_p(var_c1)
    print(type(var_p))
    print(var_p)


    var_c = am37.g_to_c(var_g,'NM_000059.3')
    print(type(var_c))
    print(var_c)


def main():
    hgvsparser = hgvs.parser.Parser() # hp

    #var_CodingDNA = hgvsparser.parse_hgvs_variant('NC_000007.13:g.21726874G>A')
    var_CodingDNA = hgvsparser.parse_hgvs_variant('NM_000059.3:c.6373dupA')
    print(var_CodingDNA)
    # SequenceVariant(ac=NC_000007.13, type=g, posedit=21726874G>A)
    print(var_CodingDNA.ac) # NC_000007.13
    print(var_CodingDNA.type) # g
    print(var_CodingDNA.posedit) # 6373dupA
    print(var_CodingDNA.posedit.pos.start) # 6373
    print(var_CodingDNA.posedit.pos.end) # 6373
    
    hdp = hgvs.dataproviders.uta.connect()#
    hgvs_dataprovider_normalized = hgvs.normalizer.Normalizer(hdp) # 用于变异的标准化 # hn
    GRCh37_genome = AssemblyMapper(hdp, assembly_name='GRCh37', alt_aln_method='splign')# GRCh37,GRCh38 ;alt_aln_method='splign';alt_aln_method='blat'
    #GRCh38_genome = AssemblyMapper(hdp, assembly_name='GRCh38', alt_aln_method='splign')# GRCh37,GRCh38 ;alt_aln_method='splign';alt_aln_method='blat'
    
    # CodingDNA to Genomic_DNA
    var_Genomic_DNA = GRCh37_genome.c_to_g(var_CodingDNA)
    print(str(var_Genomic_DNA)) # NC_000013.10:g.32914865dup

    # CodingDNA to Protein
    var_Protein = GRCh37_genome.c_to_p(var_CodingDNA)
    print(str(var_Protein)) # NP_000050.2:p.(Thr2125AsnfsTer4)

    # 获得变异相关的转录组
    print(GRCh37_genome.relevant_transcripts(var_Genomic_DNA))
    # ['NM_000059.3']

    # Genomic_DNA to CodingDNA
    var_CodingDNA = GRCh37_genome.g_to_c(var_Genomic_DNA,tx_ac='NM_000059.3')
    print(str(var_CodingDNA)) # NM_000059.3:c.6373dup


    # Normalizing variants # CodingDNA
    #var_CodingDNA_test = hgvsparser.parse_hgvs_variant("NM_001166478.1:c.30_31insT")
    Any_Variation = hgvsparser.parse_hgvs_variant("NC_000013.10:g.32914865dup")
    # var_Normalized_CodingDNA = str(normalized_hgvsparser.normalize(var_CodingDNA_test))
    Variation_Normalized_CodingDNA = Normalizing_Genomic_Variation(hgvs_dataprovider_normalized,Any_Variation)

    print(Variation_Normalized_CodingDNA)

    # Validating variants
    hgvs_validator = hgvs.validator.Validator(hdp)
    print(hgvs_validator.validate(hgvsparser.parse_hgvs_variant("NM_001166478.1:c.30_31insT")))
    # True

    try:
        hgvs_validator.validate(hgvsparser.parse_hgvs_variant("NM_001166478.1:c.30_32insT"))
    except HGVSError as e:
        print(e)
    
    # Automated liftover of NM_001261456.1:c.1762A>G (rs509749) to NM_001261457.1 via GRCh37
    
    '''
    Automatically project variant from one transcript to another via common reference.
    http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=509749
    '''
    var_c1 = hgvsparser.parse_hgvs_variant('NM_001261456.1:c.1762A>G')
    pj = hgvs.projector.Projector(hdp=hdp,
                              alt_ac='NC_000001.10',
                              src_ac=var_c1.ac,
                              dst_ac='NM_001261457.1')
    print(pj.project_variant_forward(var_c1))

    
    # Function 
    var_genomic_DNA,var_protein = hgvs2gp(var_CodingDNA,GRCh37_genome)
    print(var_genomic_DNA,var_protein)



if __name__ == '__main__':
    main()

