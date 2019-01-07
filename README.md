# Harbormaster-resource

Tracks the targets created by harbormaster which belong to a given build step and their associated diffs and revisions in [phabricator](https://secure.phabricator.com).

## Deploying to concourse

```
resource_types:
- name: harbormaster-resource
  type: docker-image
  source:
    repository: goddenrich/harbormaster-resource
    tag: latest
```

## Source Configuration

* `conduit_uri`: *Required.* The uri of the phabricator api.

* `conduit_token`: *Required.* The token to use to authenticate the conduit api call.

* `buildStepPHID`: *Required.* The phid of the build step to track targets against.

* `repo_uri`: *Required.* The uri of the git repo.

* `private_key`: *Optional.* Private key to use when pulling/pushing.
    Example:
    ```
    private_key: |
      -----BEGIN RSA PRIVATE KEY-----
      MIIEowIBAAKCAQEAtCS10/f7W7lkQaSgD/mVeaSOvSF9ql4hf/zfMwfVGgHWjj+W
      <Lots more text>
      DWiJL+OFeg9kawcUL6hQ8JeXPhlImG6RTUffma9+iGQyyBMCGd1l
      -----END RSA PRIVATE KEY-----
    ```

* `username`: *Optional.* Username for HTTP(S) auth when pulling/pushing.
  This is needed when only HTTP/HTTPS protocol for git is available (which does not support private key auth)
  and auth is required.

* `password`: *Optional.* Password for HTTP(S) auth when pulling/pushing.

* `skip_ssl_verification`: *Optional.* Skips git ssl verification by exporting
  `GIT_SSL_NO_VERIFY=true`.

* `git_config`: *Optional.* If specified as (list of pairs `name` and `value`)
  it will configure git global options, setting each name with each value.

  This can be useful to set options like `credential.helper` or similar.

  See the [`git-config(1)` manual page](https://www.kernel.org/pub/software/scm/git/docs/git-config.html)
  for more information and documentation of existing git options.

* `https_tunnel`: *Optional.* Information about an HTTPS proxy that will be used to tunnel SSH-based git commands over.
  Has the following sub-properties:
    * `proxy_host`: *Required.* The host name or IP of the proxy server
    * `proxy_port`: *Required.* The proxy server's listening port
    * `proxy_user`: *Optional.* If the proxy requires authentication, use this username
    * `proxy_password`: *Optional.* If the proxy requires authenticat, use this password

### Example

Resource configuration for a private repo with an HTTPS proxy:

``` yaml
resource_types:
- name: harbormaster-resource
  type: docker-image
  source:
    repository: goddenrich/harbormaster-resource
    tag: latest

resources:
- name: harbormaster-target
  type: harbormaster-resource
  source:
    conduit_uri: https://secure.phabricator.com/
    conduit_token: secret-token-xxxxxx
    repo_uri: git@github.com:concourse/git-resource.git
    private_key: |
      -----BEGIN RSA PRIVATE KEY-----
      MIIEowIBAAKCAQEAtCS10/f7W7lkQaSgD/mVeaSOvSF9ql4hf/zfMwfVGgHWjj+W
      <Lots more text>
      DWiJL+OFeg9kawcUL6hQ8JeXPhlImG6RTUffma9+iGQyyBMCGd1l
      -----END RSA PRIVATE KEY-----
    git_config:
    - name: core.bigFileThreshold
      value: 10m
    https_tunnel:
      proxy_host: proxy-server.mycorp.com
      proxy_port: 3128
      proxy_user: myuser
      proxy_password: myverysecurepassword
```

Create a branch with the patch of the diff associated with the target found:

``` yaml
- get: harbormaster-target
```

## Behavior

### `check`: Check for new targets.

The phabricator api (conduit) is accessed to get any targets that have been created
since the one in the latest version. If no version is given, the most recent target
(and its associated data) is returned.

### `in`: Checkout the diff associated with the target:
Clone the repository with two branches: master and pr (checked out). pr contains the diff
associated with the target and master contains the default branch of the repo.

This currently only works if you have a staging area contained within the repo itself.

### `out`: No op (for now)

Currently no-op but plan to return the outcome of the build to phabricator.

## Development

### Prerequisites

* docker is *required*

### Running the tests

Run the tests with the following command:

```sh
docker build -t harbormaster-resource .
```

### Contributing

Please make all pull requests to the `master` branch and ensure tests pass
locally.
