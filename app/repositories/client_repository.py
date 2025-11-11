from typing import Dict, Optional, List
from app.models.client import Client

class ClientRepository:
    def __init__(self):
        self._clients: Dict[int, Client] = {}
        self._next_id = 1
    
    def save(self, client: Client) -> Client:
        client.client_id = self._next_id
        self._clients[self._next_id] = client
        self._next_id += 1
        return client
    
    def find_by_id(self, client_id: int) -> Optional[Client]:
        return self._clients.get(client_id)
    
    def find_all(self) -> List[Client]:
        return list(self._clients.values())

# Singleton instance
client_repository = ClientRepository()
