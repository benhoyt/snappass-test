# snappass-test

This is a test charm for Pinterest's [SnapPass](https://github.com/pinterest/snappass) that uses the Python Operator Framework and K8s sidecar containers with [Pebble](https://github.com/canonical/pebble).


## Deploying

Before deploying the charm, make sure you have a MicroK8s environment bootstrapped, and add a model:

```
$ juju bootstrap microk8s
Creating Juju controller "microk8s-localhost" on microk8s/localhost
...
$ juju add-model snappass
Added 'snappass' model on microk8s/localhost with credential 'microk8s' for user 'admin'
```

You can now deploy the charm directly from Charmhub (you must be using Juju 2.9-rc11 or later):

```
$ juju deploy snappass-test
Located charm "snappass-test" in charm-hub, revision 9
Deploying "snappass-test" from charm-hub charm "snappass-test", revision 9 in channel stable
```

After a while `juju status` should say something like this and (after a few seconds) give you an IP address:

```
$ juju status
Model     Controller          Cloud/Region        Version   SLA          Timestamp
snappass  microk8s-localhost  microk8s/localhost  2.9-rc12  unsupported  12:07:29+12:00

App            Version  Status  Scale  Charm          Store     Channel  Rev  OS          Address  Message
snappass-test           active      1  snappass-test  charmhub  stable     8  kubernetes           snappass started

Unit              Workload  Agent  Address      Ports  Message
snappass-test/0*  active    idle   10.1.147.97         snappass started
```

Visit that IP address at port 5000 in your browser and you should see the SnapPass web UI. For example, `http://10.1.147.97:5000/`


## Building and uploading this charm

I've already uploaded this charm to Charmhub, so you shouldn't need to do this. But for reference, here are the `charmcraft` commands I used to build and upload (with charmcraft latest/edge: 0.10.0 2021-04-20):

```
$ charmcraft build
Created 'snappass-test.charm'.
$ charmcraft upload snappass-test.charm
Revision 8 of 'snappass-test' created
$ charmcraft upload-resource --image benhoyt/snappass-test snappass-test snappass-image
Revision 3 created of resource 'snappass-image' for charm 'snappass-test'
$ charmcraft upload-resource --image redis snappass-test redis-image
Revision 3 created of resource 'redis-image' for charm 'snappass-test'
$ charmcraft release snappass-test --revision=8 --resource=snappass-image:3 --resource=redis-image:3 --channel=edge --channel=stable
Revision 8 of charm 'snappass-test' released to edge, stable (attaching resources: 'snappass-image' r3, 'redis-image' r3)
```
