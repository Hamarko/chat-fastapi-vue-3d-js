from typing import List
import json
from anyio import current_effective_deadline

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class MassegData:
    def __init__(self) -> None:
        self.from_id = ''
        self.to_id = ''
        self.message = ''
        
    def to_dict(self):        
        return {
            'type_action': 'message',
            'from_id': self.from_id,
            'to_id': self.to_id,
            'message': self.message
        }

    def to_json(self):
        return json.dumps({
            'type_action': 'message',
            'from_id': self.from_id,
            'to_id': self.to_id,
            'message': self.message
        })

class ChartGraphData:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.link_update_id = None
    
    def add_node(self,client_id: str):
        self.nodes.append({"id": client_id})
    
    def update_links(self, send_data: object):
        newLinks = True
        index=0
        for link in self.links:            
            not_changed = link['source'] == send_data.from_id and link['target'] == send_data.to_id
            changed = link['source'] == send_data.to_id and link['target'] == send_data.from_id
            if changed:               
                link['source']=send_data.from_id
                link['target']=send_data.to_id               
                newLinks = False
                self.link_update_id = send_data.from_id
            if not_changed:
                newLinks = False
                self.link_update_id = send_data.from_id
            index+=1
        if newLinks:
            self.links.append({
                'source': send_data.from_id,
                'target': send_data.to_id
            })
            self.link_update_id = send_data.from_id

    def delete_node(self,client_id: str):
        
        for node in self.nodes:
            if node.get("id") == client_id:
                self.nodes.remove(node)

        self.delete_links(client_id)

    def delete_links(self,client_id: str):
        for link in self.links:
            if link.get('source') == client_id or link.get('target') == client_id:
                self.links.remove(link)

    def get_dict(self):
        return {
            'nodes': self.nodes,
            'links': self.links,
            'link_update_id': self.link_update_id
        }

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        for connections in self.active_connections:
            await self.add_user(connections.get("websocket"), client_id)        
        self.active_connections.append({'id':client_id, 'websocket': websocket})
        await self.create_user(websocket)

    async def disconnect(self, websocket):   
        client_id = ''     
        for connections in self.active_connections:
            if connections.get("websocket") == websocket:
                self.active_connections.remove(connections)
                client_id = connections.get("id")
        for connections in self.active_connections:
            data_send_users =  {
                'type_action':'users-delet',
                'users_delet':{'id': client_id, 'select': False},   
            }
            data = json.dumps(data_send_users)
            await connections.get("websocket").send_text(data) 

    async def send_personal_message(self, data: object, client_id: str):        
        for connection in self.active_connections:
            if connection.get('id') == client_id:
                await connection['websocket'].send_text(data.to_json())

    async def send_chart_data(self, data: dict):

        for connection in self.active_connections:
            await connection.get('websocket').send_text(json.dumps(data))    
    
    async def add_user(self, websocket: WebSocket, client_id: str):        
        data_send_users =  {
            'type_action':'users-add',
            'users':{'id': client_id, 'select': False}           
        }
        data = json.dumps(data_send_users)
        await websocket.send_text(data)
    
    async def create_user(self, websocket: WebSocket):
        users = []
        for item in self.active_connections:
            if item.get("websocket") != websocket:
                users.append({'id': item.get("id"), 'select': False})
        data_send_users =  {
            'type_action':'users-create',
            'users': users          
        }
        data = json.dumps(data_send_users)
        await websocket.send_text(data)

manager = ConnectionManager()
chart_data = ChartGraphData()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    chart_data.add_node(client_id)
    sending_chart_node = chart_data.get_dict()
    sending_chart_node["type_action"] = "chart_add_node"
    await manager.send_chart_data(sending_chart_node)

    try:
        while True:
            data_string = await websocket.receive_text()
            data_dict = json.loads(data_string).get("message_data")
            if data_dict.get("message") and data_dict.get("to_user_id"):                
                message = data_dict.get("message")
                to_user_id = data_dict.get("to_user_id")

                send_data = MassegData()
                send_data.from_id = client_id
                send_data.to_id = to_user_id
                send_data.message = f"You wrote: {message}"

                await manager.send_personal_message(send_data, client_id)

                chart_data.update_links(send_data)

                send_data.message = f"User ID {client_id} wrote: {message}"
                await manager.send_personal_message(send_data, to_user_id)

                sending_chart_data = chart_data.get_dict()
                sending_chart_data['type_action'] = 'chart_send_message'
                await manager.send_chart_data(sending_chart_data)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        chart_data.delete_node(client_id)
        sending_chart_data = chart_data.get_dict()
        sending_chart_data['type_action'] = 'chart_delete_node'
        await manager.send_chart_data(sending_chart_data)       