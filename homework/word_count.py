"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os
import shutil
import string
import time
from itertools import groupby

from toolz.itertoolz import concat


def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""
    os.makedirs("files/input", exist_ok=True)
    archivos_raw = glob.glob("files/raw/*")
    
    for i in range(n):
        for archivo in archivos_raw:
            nombre_base = os.path.basename(archivo)
            nombre, ext = os.path.splitext(nombre_base)
            destino = f"files/input/{nombre}_{i}{ext}"
            shutil.copyfile(archivo, destino)


def load_input(input_directory):
    """Funcion load_input"""
    archivos = glob.glob(f"{input_directory}/*")
    with fileinput.input(files=archivos) as f:
        return [line for line in f]


def preprocess_line(x):
    """Preprocess the line x"""
    x = x.lower()
    x = x.translate(str.maketrans("", "", string.punctuation))
    return x.strip()


def map_line(x):
    """Map line"""
    return [(palabra, 1) for palabra in x.split()]


def mapper(sequence):
    """Mapper"""
    procesado = map(preprocess_line, sequence)
    mapeado = map(map_line, procesado)
    return list(concat(mapeado))


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence, key=lambda x: x[0])


def compute_sum_by_group(group):
    """Compute sum by group"""
    key, iterador_valores = group
    total = sum(valor[1] for valor in iterador_valores)
    return (key, total)


def reducer(sequence):
    """Reducer"""
    grupos = groupby(sequence, key=lambda x: x[0])
    return [compute_sum_by_group(grupo) for grupo in grupos]


def create_directory(directory):
    """Create Output Directory"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def save_output(output_directory, sequence):
    """Save Output"""
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


def create_marker(output_directory):
    """Create Marker"""
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        pass


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":
    copy_raw_files_to_input_folder(n=1000)
    
    start_time = time.time()
    
    run_job(
        "files/input",
        "files/output",
    )
    
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")