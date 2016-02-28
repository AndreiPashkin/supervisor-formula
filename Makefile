snapshot:
	$(eval TAG:=`git ls-remote --tags https://github.com/saltstack/salt.git | sed -n -e 's/.*refs\/tags\/\(v$(SALT_VERSION)[.0-9]*\)$$$$/\1/p' | sort | tail -n1 | tr -d '\n'`)
	cd ./tests/ && \
	vagrant destroy -f && \
	vagrant up && \
	vagrant ssh -c "sudo apt-get update && sudo apt-get install --no-install-recommends -y python-pip" && \
	vagrant ssh -c "wget -nv -O - https://bootstrap.saltstack.com | sudo sh -s - -P git $(TAG)" && \
	vagrant ssh -c "sudo cp /project/tests/minion /etc/salt/minion'" && \
	vagrant ssh -c "sudo mkdir -p /root/.ssh/ && sudo cp ~vagrant/.ssh/authorized_keys /root/.ssh && sudo chmod 700 /root/.ssh" && \
	vagrant snapshot save $(SNAPSHOT)

ssh_config:
	(cd ./tests/ && vagrant ssh-config --host 'localhost') > $(SSH_CONFIG)
	sed -i 's/User .*/User root/g' $(SSH_CONFIG)
