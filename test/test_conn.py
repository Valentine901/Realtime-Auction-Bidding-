from app.realtime.manager import ConnectionManager

class FakeSocket:
    def __init__(self) -> None:
        self.accepted = False
        self.sent = []
        self.personal_messages = []

    async def accept(self):
        self.accepted = True

    async def send_json(self, message):
        self.sent.append(message)

    async def send_personal(self, message: dict):
        self.personal_messages.append(message)

    async def close(self, close=1000):
        pass

async def setup_conn():
    manager = ConnectionManager()
    conn1, conn2, = FakeSocket(), FakeSocket()
    return manager, conn1, conn2
    
async def test_broadcast_reaches_only_the_people_in_room():
    manager = ConnectionManager()

    ada, tunde, bola = FakeSocket(), FakeSocket(), FakeSocket()

    await manager.connect(5, ada)
    await manager.connect(5, tunde)
    await manager.connect(2, bola)

    print(manager.rooms[5])

    await manager.broadcast(5, {"type": "Hello room 5"})
    await manager.broadcast(2, {"type": "Hi room 2"})
    
    assert ada.sent == [{"type": "Hello room 5"}]
    assert bola.sent == [{"type":"Hi room 2"}]

async def test_count_conn_per_room(session):
    manager, conn1, conn2 = await setup_conn()
    await manager.connect(1, conn1)
    await manager.connect(1, conn2)
    total = manager.count_conn(1)
    assert total is 2 

async def test_send_personal_message(session):
    manager, conn1, _ = await setup_conn()
    await manager.connect(1, conn1)
    sent = await manager.send_personal(conn1, {"message":"This is your own special message"})
    assert sent is None
