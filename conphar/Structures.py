__version__ = "0.1.0"
__author__  = "https://github.com/AngelRuizMoreno"

import os, requests
import numpy as np
import pandas as pd

from io import StringIO
from pymol import cmd

__all__=['search_uniprot', 'fetch_structure']

def search_uniprot(query:str):
    """Search the UniProt database for entries matching a query.

    This function uses the UniProt REST API to perform a text search on the UniProtKB data set and retrieve the entries that match the query. The function also allows to specify the fields to be returned and the format of the output. The function returns a pandas DataFrame with the results.

    Args:
        query (str): A string containing the query to be searched in UniProtKB. The query can use UniProt's advanced search syntax.

    Returns:
        pd.DataFrame: A DataFrame with the columns corresponding to the fields specified in the code. The columns are renamed according to a dictionary defined in the code. The DataFrame is sorted by annotation score in descending order and has no duplicates.

    Example:
        >>> search_uniprot('name:insulin AND organism:"Homo sapiens (Human) [9606]"')
        # A DataFrame with 10 rows and 37 columns is returned, containing information about human insulin proteins.
    """
    
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
    """Fetch and align a protein structure from the PDB with a reference structure.

    This function uses the PyMOL command line interface to fetch a protein structure from the PDB and align it with a reference structure. The function also allows to extract the ligands from the target structure and save them to a separate file. The function returns a pandas DataFrame with the alignment statistics.

    Args:
        target (str): The PDB code of the target protein structure.
        target_chain (str): The chain identifier of the target protein structure.
        reference (str): The PDB code of the reference protein structure.
        reference_chain (str): The chain identifier of the reference protein structure.
        output_folder (str): The folder name where the output files will be saved.
        extract_ligands (bool, optional): A boolean indicating whether to extract the ligands from the target structure or not. Defaults to True.

    Returns:
        pd.DataFrame: A DataFrame with one row and eight columns containing the following information:
            - refined_RMSD: The root mean square deviation of the refined alignment in angstroms.
            - refined_num_atoms: The number of atoms used in the refined alignment.
            - n_cycles: The number of cycles performed in the alignment algorithm.
            - raw_RMSD: The root mean square deviation of the raw alignment in angstroms.
            - raw_num_atoms: The number of atoms used in the raw alignment.
            - aligment_score: The alignment score based on the BLOSUM62 matrix.
            - n_residues_aligned: The number of residues aligned between the target and reference structures.
            - lig_n_atoms: The number of atoms in the extracted ligands (only if extract_ligands is True).

    Example:
        >>> fetch_structure('1a2b', 'A', '1c3d', 'B', 'output', extract_ligands=True)
        # A DataFrame with one row and eight columns is returned, containing information about the alignment and ligand extraction of 1a2b_A with 1c3d_B.
    """
    
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
        cmd.remove(f"solvent or inorganic or resn PEG or resn DMS or resn GOL or resn FTM or (not alt ''+{target_chain})")
        n_lig=cmd.select('Ligand', state=1, selection=(f'byres chain {target_chain} and (organic or hetatm)'))

        data.loc[target,'lig_n_atoms']=n_lig
        
        cmd.save(f"{output_ligand}/{target}_lig.sdf",selection='Ligand',format='sdf')

        cmd.remove('solvent or inorganic or organic')
        cmd.save(f"{output_receptor}/{target}_{target_chain}.pdb",selection='target',format='pdb')

    else:
        cmd.save(f"{output_receptor}/{target}_{target_chain}.pdb",selection='target',format='pdb')


    cmd.delete('all')
    
    return data