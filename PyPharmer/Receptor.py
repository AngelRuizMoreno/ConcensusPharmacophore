import os, requests
import numpy as np
import pandas as pd

from io import StringIO
from pymol import cmd

__all__=['search_uniprot', 'fetch_structure']

def search_uniprot(query:str):
    
    fields={'accession':'ACCESION',
                'id':'ENTRY_id',
                'reviewed':'STATUS', 
                'annotation_score':'SCORE',
                'protein_existence':'EXISTENCE',
                'protein_name':'PROTEIN_name',
                'cc_function':'FUNCTION',
                'gene_primary':'GENE_name',
                'xref_geneid':'GENE_id',
                'xref_refseq' : 'REFSEQ',
                'organism_name':'ORGANISM_name',
                'organism_id':'ORGANISM_id',
                'lineage' : 'LINEAGE',
                'ec':'EC',
                'go_p':'GO_process',
                'go_c':'GO_component',
                'go_f':'GO_function',
                'protein_families':'PROTEIN_families',
                'ft_domain':'FEATURE_domain',
                'ft_motif':'FEATURE_motif',
                'cc_domain':'COMMENT_domain',
                'ft_topo_dom' : 'DOMAIN_topological',
                'xref_pdb':'PDB',
                'xref_kegg':'KEGG',
                'xref_biocyc':'BIOCYC',
                'xref_interpro':'INTERPRO',
                'xref_pfam':'PFAM',
                'ft_act_site':'FEATURE_active_site',
                'ft_site':'FEATURE_site',
                'ft_binding':'FEATURE_binding',
                'cc_catalytic_activity':'CATALYTIC_activity',
                'rhea':'RHEA',
                'length':'LENGTH',
                'sequence':'SEQUENCE'}
    
    
    URL=f"https://rest.uniprot.org/uniprotkb/search?fields={','.join(fields.keys())}&format=tsv&query={query}&size=500"
    results=[]
    r=requests.get(URL)
    results.append(r.text)
    
    if 'next' in r.links.keys():
        repeat=True
    else:
        repeat=False

    while repeat:
        r=requests.get(r.links['next']['url'])
        results.append(r.text)
        if 'next' in r.links.keys():
            repeat=True
        else:
            repeat=False
    
    if len(results)>=1:
        uniprot_data = pd.concat([pd.read_csv(StringIO(result), sep='\t') for result in results])
        uniprot_data.drop_duplicates(inplace=True,ignore_index=True)
        uniprot_data.columns=fields.values()
        uniprot_data.sort_values(by='SCORE',ascending=False,ignore_index=True,inplace=True)
    else:
        uniprot_data=None
    
    return uniprot_data

def fetch_structure(target:str,target_chain:str,reference:str, reference_chain:str, output_folder:str,extract_ligands:bool=True):
    
    output_receptor=os.path.join(output_folder,'receptor')
    output_ligand=os.path.join(output_folder,'ligand')
    
    if os.path.exists(output_receptor) == False:
        os.mkdir(output_receptor)
    
    if os.path.exists(output_ligand) == False:
        os.mkdir(output_ligand)
    
    cmd.fetch(reference,name='reference',type='pdb1')
    cmd.remove('solvent or inorganic or organic')
    cmd.select(f'ref_structure',selection=f'chain {reference_chain}')
    cmd.fetch(target,name='target',type='pdb1')
    cmd.select('tar_structure',selection=f"target and chain {target_chain}")
    
    rmsd= cmd.align('tar_structure','ref_structure', cutoff=2.0, cycles=5, matrix='BLOSUM62',  mobile_state=1, target_state=1)
    arr=np.array(rmsd)
    data=pd.DataFrame(arr.reshape(1,-1), columns=['refined_RMSD','refined_num_atoms','n_cycles','raw_RMSD','raw_num_atoms','aligment_score','n_residues_aligned'],index=[target])

    if extract_ligands:         
        cmd.remove(f"solvent or inorganic or resn DMS or resn GOL or resn FTM or (not alt ''+{target_chain})")
        n_lig=cmd.select('Ligand', state=1, selection=(f'byres ((chain {target_chain} and (resi 145 or resi 41) expand 10 and organic and not resn EDO or not chain {target_chain} and not chain B))'))

        data.loc[target,'lig_n_atoms']=n_lig
        
        cmd.save(f"{output_ligand}/{target}_lig.sdf",selection='Ligand',format='sdf')

        cmd.remove('solvent or inorganic or organic')
        cmd.save(f"{output_receptor}/{target}_{target_chain}.pdb",selection='target',format='pdb')

    else:
        cmd.save(f"{output_receptor}/{target}_{target_chain}.pdb",selection='target',format='pdb')


    cmd.delete('all')
    
    return data