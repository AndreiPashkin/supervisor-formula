snapshot:
	cd ./tests/ && \
	vagrant destroy -f && \
	vagrant up && \
	vagrant ssh -c "which pip || (sudo apt-get update && sudo apt-get install --no-install-recommends -y python-pip)" && \
	vagrant ssh -c "sudo cp /project/tests/minion /etc/salt/minion" && \
	vagrant ssh -c "sudo mkdir -p /root/.ssh/ && sudo cp ~vagrant/.ssh/authorized_keys /root/.ssh && sudo chmod 700 /root/.ssh" && \
	vagrant snapshot save $(SNAPSHOT)

ssh_config:
	(cd ./tests/ && vagrant ssh-config --host 'localhost') > $(SSH_CONFIG)
	sed -i 's/User .*/User root/g' $(SSH_CONFIG)
