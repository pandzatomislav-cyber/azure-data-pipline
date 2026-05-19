from azure.storage.blob import BlobServiceClient
import os


def get_client() -> BlobServiceClient:
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise EnvironmentError("AZURE_STORAGE_CONNECTION_STRING is not set.")
    return BlobServiceClient.from_connection_string(conn_str)


def ensure_container(client: BlobServiceClient, name: str) -> None:
    try:
        client.create_container(name)
        print(f"[AZURE] Created container: {name}")
    except Exception:
        pass  # Container already exists


def upload_blob(container: str, blob_name: str, data: bytes) -> str:
    client = get_client()
    ensure_container(client, container)
    blob_client = client.get_blob_client(container=container, blob=blob_name)
    blob_client.upload_blob(data, overwrite=True)
    url = blob_client.url
    print(f"[UPLOAD] {blob_name} -> {container} ({len(data):,} bytes)")
    return url


def download_blob(container: str, blob_name: str) -> bytes:
    client = get_client()
    blob_client = client.get_blob_client(container=container, blob=blob_name)
    data = blob_client.download_blob().readall()
    print(f"[DOWNLOAD] {blob_name} <- {container} ({len(data):,} bytes)")
    return data
