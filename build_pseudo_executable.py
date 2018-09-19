# Para rodar: python3.6 .\build_pseudo_executable.py build_ext --inplace

import shutil
import os
import glob
import distutils

from distutils.core import setup
from Cython.Distutils import build_ext
from distutils.extension import Extension

PSEUDO_EXECUTABLE_DIR = os.path.join(".", "pseudo_executable")
LIBS_DIR = os.path.join(".venv", "Lib", "site-packages")


def main():
    setup(
        name = 'MyProject',
        cmdclass = {'build_ext': build_ext},
        ext_modules = [
            Extension("main", ["main.py"]),
            Extension("data_fetcher", ["data_fetcher.py"]),
            Extension("data_writer", ["data_writer.py"]),
            Extension("custom_writers.caps_writer", ["custom_writers\caps_writer.py"]),
            Extension("custom_writers.stingy_writer", ["custom_writers\stingy_writer.py"])
        ]
    )

    # Criando o diretório que conterá o pseudo executável
    if os.path.exists(PSEUDO_EXECUTABLE_DIR):
        shutil.rmtree(PSEUDO_EXECUTABLE_DIR)
    os.makedirs(PSEUDO_EXECUTABLE_DIR)

    # Copiando os arquivos .pyd para o diretorório do pseudo executável
    pyd_files = glob.glob('**/*.pyd', recursive=True)
    for file_relative_path in pyd_files:
        dest = os.path.join(PSEUDO_EXECUTABLE_DIR, file_relative_path)
        try:
            shutil.copy(file_relative_path, dest)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(dest))
            shutil.copy(file_relative_path, dest)

    # Criando o arquivo main.py (arquivo que deve ser chamado para iniciar o programa)
    with open(os.path.join(PSEUDO_EXECUTABLE_DIR, "main.py"),'w') as f:
        f.write("""from main import main\n\nif __name__ == "__main__":\n\tmain()\n""")

    # Copiando as libs que estão no virtualenv
    distutils.dir_util.copy_tree(LIBS_DIR, PSEUDO_EXECUTABLE_DIR)

    # Limpando os arquivos temporários criados pelo cython
    if os.path.exists("build"):
        shutil.rmtree("build")
    for file_relative_path in glob.glob('**/*.c', recursive=True):
        os.remove(file_relative_path)
    for file_relative_path in pyd_files:
        os.remove(file_relative_path)

if __name__ == "__main__":
    main()
