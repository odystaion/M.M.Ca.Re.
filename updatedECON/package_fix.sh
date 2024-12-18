pip uninstall torch
pip uninstall torchvision
pip uninstall pytorch-lightning
pip uninstall trimesh

pip install torch==1.13.1
pip install torchvision==0.14.1
pip install pytorch-lightning==1.9.0
pip install trimesh==4.3

cp /content/mm-care/__init__.py /usr/local/envs/econ/lib/python3.8/site-packages/chumpy/__init__.py