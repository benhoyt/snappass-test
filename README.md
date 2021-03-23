# snappass-test

This is a test charm for Pinterest's [SnapPass](https://github.com/pinterest/snappass) that uses the Python Operator Framework and K8s sidecar containers with [Pebble](https://github.com/canonical/pebble).

Due to issues with Charmhub resources and `metadata.yaml` v2 handling, this does not yet deploy via the Charmhub store -- these will be fixed soon. In the meantime, you need to build the charm and deploy it locally:

```
$ git clone https://github.com/benhoyt/snappass-test
$ cd snappass-test
$ charmcraft build
Created 'snappass-test.charm'.
```

You'll need version 1.14 or later of Go (`go version` will confirm your current version), and the latest Juju 2.9 release. Or you can build Juju from source:

```
$ git clone -b 2.9 https://github.com/juju/juju
$ cd juju
$ make install
$ make microk8s-operator-update  # to make the microk8s image and push to Docker
$ export PATH="/home/${USER}/go/bin:$PATH"
```

Before doing `juju deploy`, make sure you have a MicroK8s environment bootstrapped (`juju bootstrap microk8s`), then change to the `snappass-test` directory. For now, you need to specify the resources manually with `--resource`:

```
$ juju deploy ./snappass-test.charm --resource snappass-image=benhoyt/snappass-test --resource redis-image=redis
Located local charm "snappass-test", revision 0
Deploying "snappass-test" from local charm "snappass-test", revision 0
```

After a while `juju status` should say something like this and (after a few seconds) give you an IP address:

```
$ juju status
Model     Controller           Cloud/Region        Version  SLA          Timestamp
snappass  microk8s-localhost2  microk8s/localhost  2.9-rc7  unsupported  14:07:40+13:00

App            Version  Status  Scale  Charm          Store  Channel  Rev  OS      Address  Message
snappass-test           active      1  snappass-test  local             0  ubuntu           snappass started

Unit              Workload  Agent  Address      Ports  Message
snappass-test/0*  active    idle   10.1.147.84         snappass started
```

Visit that IP address at port 5000 in your browser and you should see the SnapPass web UI. For example, `http://10.1.147.69:5000/`
