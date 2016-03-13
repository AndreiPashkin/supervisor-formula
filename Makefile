run: require-CONTAINER
	- sudo lxc-start -n $(CONTAINER)

copy-files: require-CONTAINER run
	sudo lxc-attach -n $(CONTAINER) -- mkdir -p /salt/ /etc/salt/
	tar -c ./supervisor | sudo lxc-attach -n $(CONTAINER) -- /bin/sh -c "tar -C /salt/ -x"
	tar -C ./tests/salt -c . | sudo lxc-attach -n $(CONTAINER) -- /bin/sh -c "tar -C /salt/ -x"
	tar -C ./tests/ -c minion | sudo lxc-attach -n $(CONTAINER) -- /bin/sh -c "tar -C /etc/salt/ -x"

provision: require-CONTAINER require-SALT_VERSION run
	sudo lxc-attach -n $(CONTAINER) -- sh -c "which pip curl || sudo apt-get update && sudo apt-get install --no-install-recommends -y --force-yes python-pip curl"
	sudo lxc-attach -n $(CONTAINER) -- sh -c "curl -L https://bootstrap.saltstack.com | sudo sh -s -- stable $(SALT_VERSION)"

snapshot: require-CONTAINER
	- sudo lxc-stop -n $(CONTAINER)
	sudo lxc-snapshot -n $(CONTAINER)

require-CONTAINER:
ifndef CONTAINER
	$(error CONTAINER is undefined)
endif

require-SALT_VERSION:
ifndef SALT_VERSION
	$(error SALT_VERSION is undefined)
endif
