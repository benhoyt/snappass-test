# snappass-test

## Description

Test charm for Pinterest's SnapPass that uses Operator Framework
and K8s sidecar containers.

This does deploy via Charmhub (but you need to specify `--resource` for the images manually, because of an issue with Charmhub resources). Or you can build and deploy the charm locally:

```
$ git clone https://github.com/benhoyt/snappass-test
$ cd snappass-test
$ charmcraft build
Created 'snappass-test.charm'.
```

You'll need version 1.14 or later of Go (`go version` will confirm your current version), and a custom version of the Juju 2.9 branch, as below:

```
$ git clone -b demo-pebble https://github.com/benhoyt/juju
$ cd juju
$ make install
$ make microk8s-operator-update  # to make the microk8s image and push to Docker
$ export PATH="/home/${USER}/go/bin:$PATH"
```

When doing `juju deploy`, go to the `snappass-test` directory. You need to specify the resources manually:

```
$ juju bootstrap microk8s
$ juju add-model snappass
$ juju deploy snappass-test --resource snappass-image=benhoyt/snappass-test --resource redis-image=redis
```

Or deploy against the local charm (see build instructions above):

```
$ juju deploy ../snappass-test/snappass-test.charm snappass --resource snappass-image=benhoyt/snappass-test --resource redis-image=redis
Located local charm "snappass-test", revision 0
Deploying "snappass" from local charm "snappass-test", revision 0
```

After a while `juju status` should say something like this and (after a few seconds) give you an IP address:

```
$ juju status
Model     Controller           Cloud/Region        Version  SLA          Timestamp
snappass  microk8s-localhost2  microk8s/localhost  2.9-rc7  unsupported  07:03:51+13:00

App       Version  Status  Scale  Charm          Store  Channel  Rev  OS      Address  Message
snappass           active      1  snappass-test  local             0  ubuntu           snappass started

Unit         Workload  Agent  Address      Ports  Message
snappass/0*  active    idle   10.1.147.69         snappass started
```

Visit that IP address at port 5000 in your browser and you should see the SnapPass web UI. For example, `http://10.1.147.69:5000/`
