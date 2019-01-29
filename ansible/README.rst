To run this playbook::

   # Clone the "koji-ansible" project:
   git clone https://github.com/ktdreyer/koji-ansible

   # Symlink the "library" and "module_utils" directories to the current
   working directory:
   ln -s koji-ansible/library
   ln -s koji-ansible/module_utils

   # Run the shell script that calls ansible-playbook:
   ./run.sh
