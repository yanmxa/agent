from kubernetes import config, dynamic, client


class KubeTool:
    def __init__(self) -> None:
        # Load Kubernetes configuration and create a dynamic client
        self.kube_config = config.load_kube_config()
        self.dynamic_client = dynamic.DynamicClient(
            client.ApiClient(configuration=self.kube_config)
        )

    def discovery_api(self) -> str:
        """
        Prints the list of available API versions, similar to `kubectl api-versions`.
        """
        print("Supported APIs (* indicates preferred version):")
        for api in client.ApisApi().get_api_versions().groups:
            versions = [
                (
                    f"*{v.version}"
                    if v.version == api.preferred_version.version
                    and len(api.versions) > 1
                    else v.version
                )
                for v in api.versions
            ]
            print(f"{api.name:<40} {','.join(versions)}")

        return "TERMINATE"

    def list_resources(self, version: str, kind: str) -> str:
        """
        Lists and prints resources of a specified kind and version.

        :param version: API version of the resource.
        :param kind: Kind of the resource.
        :return: A termination string.
        """
        api = self.dynamic_client.resources.get(api_version=version, kind=kind)
        for res in api.get().items:
            print(
                {
                    "kind": res.kind,
                    "namespace": res.metadata.namespace,
                    "name": res.metadata.name,
                }
            )

        return "TERMINATE"


def termination_message(msg):
    """
    Checks if the message contains the termination string.

    :param msg: Message dictionary to check.
    :return: Boolean indicating if termination condition is met.
    """
    return msg.get("content") is not None and "TERMINATE" in msg["content"]
