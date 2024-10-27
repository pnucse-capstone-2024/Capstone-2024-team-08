import os
import pickle
from openbabel import pybel
from rdkit import Chem
from openbabel import openbabel
from vina import Vina
import numpy as np


def cal_score(ligand):
    try:
        v = Vina(sf_name='vina')
        v.set_receptor('../receptor/receptor.pdbqt')
        v.set_ligand_from_file(ligand)

        center_x, center_y, center_z = calculate_center_of_mass(ligand)
        v.compute_vina_maps(center=[center_x, center_y, center_z], box_size=[20, 20, 20])
        
        a = v.score()
        b = v.optimize()
        v.dock(exhaustiveness=8, n_poses=3)
        c = v.score()
        d = v.optimze()
        print(a[0], b[0], c[0], d[0])
        return d[0]
    except:
        return 0

def calculate_center_of_mass(pdbqt_file):
    x_coords = []
    y_coords = []
    z_coords = []

    with open(pdbqt_file, 'r') as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                x_coords.append(x)
                y_coords.append(y)
                z_coords.append(z)

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    center_z = sum(z_coords) / len(z_coords)

    return center_x, center_y, center_z

def save_data(target, filename):
    with open(filename, 'wb') as f:
        pickle.dump(target, f)

def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# PDBQT 파일을 RDKit Mol 객체로 변환하는 함수
def pdbqt_to_mol(pdbqt_file):
    mols = list(pybel.readfile("pdbqt", pdbqt_file))
    if mols:
        mol = mols[0]  # 첫 번째 분자만 사용
        pdb_block = mol.write("pdb")
        return Chem.MolFromPDBBlock(pdb_block)
    return None


if __name__ == "__main__":
    # ./ligand 디렉토리 내의 모든 PDBQT 파일 읽기
    ligand_dir = './../ligand'
    ligand_files = [f for f in os.listdir(ligand_dir) if f.endswith('.pdbqt')]
    ligand_files.sort()


    result = list()
    for ligand_file in ligand_files:
        print(ligand_file)
        ligand_path = os.path.join(ligand_dir, ligand_file)
        score = cal_score(ligand_path)
        print(score)
        result.append((score, ligand_file))

    for i in result:
        print(i)
    
    save_data(result, 'test.dat')

    # 4 27