from app.repositories.user import UserRepository
from app.models import User 



async def test_flush_gives_an_id_but_is_not_permanent(session):
    repo = UserRepository(session)
    user = User(
        fullname="ada",
        email="ada@example.com",
        password="x"
    )

    session.add(user)
    print("after add: ", user.id)

    await session.flush()
    print("after flush: ", user.id)

    await session.rollback()
    print("after rollback:", await repo.get_by_email("ada@example.com"))


async def test_get_by_email_returns_none_when_missing(session):
    repo = UserRepository(session)
    result = await repo.get_by_email("nobody@example.com")
    assert result is None

async def test_user_get_by_id(session):
    repo = UserRepository(session)
    result = await repo.get_by_id(1)
    assert result is None

# def test_greeting(greeting):
#     total = 0
#     target = 10
#     for i in range(4):
#         total += i 
#     assert total != target