from cyvcf2 import VCF

for variant in VCF('samtools.indels.vcf.gz'): # or VCF('some.bcf')
    ref_seq = variant.REF # e.g. REF='A', 
    alt_seq = variant.ALT # e.g. ALT=['C', 'T']
    chrom = variant.CHROM
    start = variant.start
    end = variant.end
    variant_id = variant.ID
    filter_string = variant.FILTER
    variant_qual = variant.QUAL

    # numpy arrays of specific things we pull from the sample fields.
    # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
    # type # numpy array
    # get_type = variant.gt_types
    # gt_ref_depths = variant.gt_ref_depths
    # gt_alt_depths = variant.gt_alt_depths
    # gt_phases = variant.gt_phases
    # gt_quals = variant.gt_quals
    # gt_bases = variant.gt_bases
    # print(get_type,gt_ref_depths)

    ## INFO Field.
    ## extract from the info field by it's name:
    info_DP = variant.INFO.get('DP') # int
    # info_FS = variant.INFO.get('FS') # float
    # info_AC = variant.INFO.get('AC') # float
    print(variant.INFO)
    # <cyvcf2.cyvcf2.INFO object at 0x7fb4d8d02f10>
    print(dict(variant.INFO))
    # {'INDEL': True, 'IDV': 1, 'IMF': 0.012345699593424797, 'DP': 81, 'I16': (45.0, 18.0, 1.0, 0.0, 3713.0, 231795.0, 54.0, 2916.0, 3780.0, 226800.0, 60.0, 3600.0, 1303.0, 31025.0, 8.0, 64.0), 'QS': (0.9843840003013611, 0.015615999698638916), 'VDB': 0.47082599997520447, 'SGB': -0.3798849880695343, 'MQSB': 1.0, 'MQ0F': 0.0}

    # convert back to a string.
    print(str(variant)) # 整行内容

 
    ## sample info...

    # Get a numpy array of the depth per sample:
    dp = variant.format('DP')
    print("dp",dp) # dp [[55]]
    print("dp shape",dp.shape)
    # or of any other format field:
    # sb = variant.format('SB')
    # assert sb.shape == (n_samples, 4) # 4-values per

# to do a region-query:

vcf = VCF('samtools.indels.vcf.gz')
for v in vcf('JX123:1-500'):
    if v.INFO["IMF"] > 0.1: continue
    print(str(v))

#Modifying Existing Records
# from cyvcf2 import VCF, Writer
# vcf = VCF(VCF_PATH)
# # adjust the header to contain the new field
# # the keys 'ID', 'Description', 'Type', and 'Number' are required.
# vcf.add_info_to_header({'ID': 'gene', 'Description': 'overlapping gene',
#     'Type':'Character', 'Number': '1'})

# # create a new vcf Writer using the input vcf as a template.
# fname = "out.vcf"
# w = Writer(fname, vcf)

# for v in vcf:
#     # The get_gene_intersections function is not shown.
#     # This could be any operation to find intersections
#     # or any manipulation required by the user.
#     genes = get_gene_intersections(v)
#     if genes is not None:
#         v.INFO["gene"] = ",".join(genes)
#     w.write_record(v)

# w.close(); vcf.close()

# Setting Genotyping Strictness

# from cyvcf2 import VCF
# vcf = VCF("/path/to/vcf/file", strict_gt=True)
# for variant in vcf:
#     # do something
#     pass



# https://github.com/brentp/cyvcf2/blob/main/docs/source/index.rst
