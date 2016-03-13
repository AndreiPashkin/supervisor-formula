snapshot:
	cd ./tests/ && \
	lxc exec $(CONTAINER) --mode=non-interactive -- sh -c "which pip curl || (sudo apt-get update && sudo apt-get install --no-install-recommends -y python-pip curl)"
	lxc exec $(CONTAINER) --mode=non-interactive -- sh -c "curl -L https://bootstrap.saltstack.com | sudo sh -s -- stable 2015.8"
	lxc file push ./tests/minion $(CONTAINER)/etc/salt/minion
	lxc config device add $(CONTAINER) share disk path=/salt/ source=$(SHARE)
	lxc snapshot $(CONTAINER) $(SNAPSHOT)
