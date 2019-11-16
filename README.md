
# ssh-key-manager
A Python script to distribute SSH public keys to remote machines

## Details
The script pushes a set of ssh public keys to a set of remote servers' authorized_keys files for the user running the script, without creating duplicate keys. The list of public keys is contained in the <username>_public_keys.txt file. Each key can have a one-line comment above it beginning with '#' that will be copied with the key.

ssh-copy-id does a similar thing but only for the public key form the current host.

## Assumptions

* The user running the script has an account on each of the hosts in the push_hostlist.txt file

* Each of the hosts in the push_hostlist.txt file is:
   * running an SSH server that the current user can log in to
   * has an authorized_keys file at ~/.ssh/authorized_keys 

## Improvements

* Read the three field of the ssh key from the downloaded authorized_keys file and check for a duplicate of the third field - this will allow a changed key to be replaced. Currently it only detects duplicates if the whole key is identical.

* Better handle the comment lines above each key - they seem to get dislocated form the key line sometimes.
