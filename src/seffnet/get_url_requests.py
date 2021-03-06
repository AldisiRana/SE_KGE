# -*- coding: utf-8 -*-

"""Handle databases url requests."""

import urllib
import urllib.parse
import urllib.request
from urllib.error import HTTPError


def get_result(url):
    """
    Get response from API.

    :param url: API url
    :return: reponse body
    """
    try:
        connection = urllib.request.urlopen(url)
    except HTTPError:
        return ""
    else:
        return connection.read().rstrip()


def cid_to_smiles(cid):
    """
    Get the SMILES for chemicals in PubChem database.

    :param cid: pubchem identifier
    :return: SMILES
    """
    return get_result("http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/canonicalSMILES/TXT" % cid)


def cid_to_inchikey(cid):
    """
    Get the inchikey for chemicals in PubChem database.

    :param cid: pubchem identifier
    :return: inchikey
    """
    return get_result("http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/InChIKey/TXT" % cid)


def smiles_to_cid(smiles):
    """
    Get the chemical pubchem ID from the SMILES.

    :param smiles: the SMILES code of a chemical
    :return: the pubchem identifier
    """
    return get_result("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/%s/cids/TXT" % smiles)


def inchikey_to_cid(inchikey):
    """
    Get the chemical pubchem ID from the inchikey.

    :param inchikey: the inchkey code of a chemical
    :return: the pubchem identifier
    """
    return get_result("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/%s/cids/TXT" % inchikey)


def cid_to_synonyms(cid):
    """
    Get the synonyms of chemical in PubChem database.

    :param cid: pubchem identifier
    :return: synonyms of the chemical
    """
    return get_result("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/synonyms/TXT" % cid)


def get_gene_names(uniprot_list, from_id='ACC+ID', to_id='GENENAME'):
    """
    Get gene names from uniport ID.

    :param uniprot_list: a list of uniprot IDs
    :return: a dictionary with the uniprotID as key and gene name as value
    """
    url = 'https://www.uniprot.org/uploadlists/'
    uniprot_ids = ''
    for prot in uniprot_list:
        uniprot_ids += prot + ' '

    params = {
        'from': from_id,
        'to': to_id,
        'format': 'tab',
        'query': uniprot_ids,
    }
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read().decode('utf-8')
    results = response.split('\n')
    dict_proteins = {}
    for string in results[1:-1]:
        pair = string.split('\t')
        dict_proteins[pair[0]] = pair[1]
    return dict_proteins
