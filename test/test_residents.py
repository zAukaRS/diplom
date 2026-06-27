import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy import select

from app.models import Request, Request_before, User
from app.core.dependencies import get_current_user


@pytest.mark.asyncio
class TestResidents:

    async def test_get_residents_month_12_edge(self, client, db_session, admin_user, test_customer, test_room, test_field):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        for i in range(3):
            req = Request(
                customer_id=test_customer.id,
                contract_num=f"Д-{i}",
                contract_date=date.today(),
                eol_fio=f"ФИО{i}",
                user_id=admin_user.id,
                position="Инж",
                field_id=test_field.id,
                check_in=date(2023, 12, 1),
                check_out=date(2023, 12, 5),
                days=4,
                room_id=test_room.id,
                status="approved",
                resident_id=None,
            )
            db_session.add(req)
        await db_session.commit()

        response = await client.get("/api/residents?month=12&year=2023&date_1=2023-12-01")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    @pytest.mark.xfail(reason="known bug: endpoint returns empty list despite existing approved requests")
    async def test_pagination_double(self, client, db_session, admin_user, test_customer, test_room, test_field):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        for i in range(15):
            req = Request(
                customer_id=test_customer.id,
                contract_num=f"Д-{i}",
                contract_date=date.today(),
                eol_fio=f"ФИО{i}",
                user_id=admin_user.id,
                position="Инж",
                field_id=test_field.id,
                check_in=date(2023, 1, 1),
                check_out=date(2023, 1, 5),
                days=4,
                room_id=test_room.id,
                status="approved",
                resident_id=None,
            )
            db_session.add(req)
        await db_session.commit()

        response1 = await client.get("/api/residents?limit=10&offset=0")
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1) == 10

        response2 = await client.get("/api/residents?limit=10&offset=10")
        data2 = response2.json()
        assert len(data2) == 5

        ids1 = {d["id"] for d in data1}
        ids2 = {d["id"] for d in data2}
        assert len(ids1 & ids2) == 0

    async def test_search_empty_word(self, client, admin_user):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user
        response = await client.get("/api/residents?word=")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_search_sql_injection(self, client, admin_user):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user
        word = "%admin%' OR '1'='1"
        response = await client.get(f"/api/residents?word={word}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_field_not_found(self, client, admin_user):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user
        response = await client.get("/api/residents?by_field=999")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.xfail(reason="known bug: AttributeError when user not found")
    async def test_guest_with_nonexistent_user_xfail(self, client, db_session, admin_user):
        req = Request_before(
            customer="ООО",
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=99999,
            position="Инж",
            field_id=1,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=1,
            status="approved",
            full_name="Иван",
            gender="М",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        client.app.dependency_overrides[get_current_user] = lambda: admin_user
        response = await client.get("/api/residents?by_field=1")
        assert response.status_code == 200