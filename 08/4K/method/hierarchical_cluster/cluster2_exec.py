import os
import pickle
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse
from vina import Vina
import random


def save_data(target, filename):
    with open(filename, 'wb') as f:
        pickle.dump(target, f)

def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
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

def cal_score(ligand, receptor):
    v = Vina(sf_name='vina')
    v.set_receptor(receptor)
    v.set_ligand_from_file(ligand)

    center_x, center_y, center_z = calculate_center_of_mass(ligand)
    v.compute_vina_maps(center=[center_x, center_y, center_z], box_size=[120, 120, 120])

    v.dock(exhaustiveness=32, n_poses=10)
    print()
    energy = v.score()
    
    return energy[0] 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docking script")
    parser.add_argument('receptor', type=str, help='Path to the receptor file')
    parser.add_argument('count', type=str, help='Docking count')
    parser.add_argument('result_tail', type=str, help='result_tail')
    parser.add_argument('folder_name', type=str, help='folder_name')
    args = parser.parse_args()
    receptor = args.receptor
    count = int(args.count)
    result_tail = int(args.result_tail)
    folder_name = args.folder_name
    receptor_path = f"./../data/receptor/{receptor}.pdbqt"
    print(receptor_path)

    cluster = load_data(f"./{folder_name}/cluster.dat")
    docking_result = load_data(f'./../data/{receptor}_docking_result.dat')
    smile_dict = load_data('./../data/smile_dict.dat')
    ligand_dir = './../data/ligand'
    ligands = list(smile_dict.keys())

    docking_cnt = 1
    cluster_result = list() 
    excluded_ligands = defaultdict(bool)
    length = len(next(iter(cluster.values())))
    last_cluster = -1
    for level in range(length):
        print(f"Level {level}")
        check_index = defaultdict(int)
        cluster_score = defaultdict(int)

        random.shuffle(ligands)
        for ligand in ligands:
            if excluded_ligands[ligand] is False:
                cluster_id = cluster[ligand][level]
                if check_index[cluster_id] < 5:
                    print(f"{ligand} {docking_cnt}/{count}, cluster index {cluster_id} ({check_index[cluster_id]+1}/5)")
                    docking_cnt += 1
                    if ligand not in docking_result:
                        ligand_path = os.path.join(ligand_dir, ligand)
                        score = cal_score(ligand_path, receptor_path)
                        docking_result[ligand] = score
                    else:
                        score = docking_result[ligand]
                        print(score)

                    cluster_result.append((score, ligand))
                    # 평균
                    # cluster_score[cluster_id] += score
                    # 최저값
                    cluster_score[cluster_id] = min(cluster_score[cluster_id], score)
                    
                    check_index[cluster_id] += 1
                    excluded_ligands[ligand] = True

        best_cluster = None
        best_score = float('inf')
        for cid, cscore in cluster_score.items():
            if cscore < best_score:
                best_score = cscore
                best_cluster = cid
        
        print(f"Level {level}'s best cluster is {best_cluster}")
        for ligand in ligands:
            if excluded_ligands[ligand] is False:
                cluster_id = cluster[ligand][level]
                if cluster_id != best_cluster:
                    excluded_ligands[ligand] = True
        tmp_cnt = 0
        for ligand in ligands:
            if excluded_ligands[ligand] is False:
                tmp_cnt += 1
        print(f"Remaining ligands {tmp_cnt}")
        print()
        last_cluster = best_cluster
    
    print(f"docking count is {docking_cnt}")
    if docking_cnt < count:
        random.shuffle(ligands)
        for ligand in ligands:
            if excluded_ligands[ligand] is False:
                cluster_id = cluster[ligand][length-1]
                if cluster_id == last_cluster:
                    print(f"{ligand} {docking_cnt}/{count}")
                    docking_cnt += 1
                    if ligand not in docking_result:
                        ligand_path = os.path.join(ligand_dir, ligand)
                        score = cal_score(ligand_path, receptor_path)
                        docking_result[ligand] = score
                    else:
                        score = docking_result[ligand]
                        print(score)

                    cluster_result.append((score, ligand))
                    if docking_cnt == count + 1:
                        break
    
    cluster_result.sort(key=lambda x: x[0])
    top_ligands = cluster_result[:10]

    print("Top10 ligands")
    for ligand in top_ligands:
        print(f"File: {ligand[1]}, Score: {ligand[0]}")
    print()
    scores = [ligand[0] for ligand in top_ligands]
    avg_score = sum(scores) / len(scores)
    print(f"Average score of top10 ligands: {avg_score: .2f}")

    save_data(cluster_result, f"./../result/{receptor}/{count}/cluster2_result{result_tail}.dat")
    save_data(docking_result, f"./../data/{receptor}_docking_result.dat")


                
