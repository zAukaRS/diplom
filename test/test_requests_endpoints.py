import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy import select

from app.models import Request_before, Request, Room, Field, User
from app.core.dependencies import get_current_user


@pytest.mark.asyncio
class TestRequestsEndpoints:

    @pytest.mark.xfail(reason="known bug: RequestCreate schema missing contract_num field")
    async def test_create_request_room_foreign_field(self, client, db_session, test_user, test_field, test_customer, test_resident):
        client.app.dependency_overrides[get_current_user] = lambda: test_user

        other_field = Field(name="Другое поле")
        db_session.add(other_field)
        await db_session.commit()
        await db_session.refresh(other_field)
        room_other = Room(
            room_number="999",
            field_id=other_field.id,
            capacity=2,
            status=0,
        )
        db_session.add(room_other)
        await db_session.commit()
        await db_session.refresh(room_other)

        payload = {
            "customer": test_customer.name,
            "contract_date": date.today().isoformat(),
            "eol_fio": "Иванов",
            "position": "Инж",
            "field_id": test_field.id,
            "check_in": date.today().isoformat(),
            "check_out": (date.today() + timedelta(days=1)).isoformat(),
            "room_id": room_other.id,
            "comment": "",
        }
        response = await client.post("/api/requests/", json=payload)
        assert response.status_code == 400

    @pytest.mark.xfail(reason="known bug: room_id not checked against field_id")
    async def test_create_request_room_foreign_field_xfail(self, client, db_session, test_user, test_field, test_customer, test_resident):
        client.app.dependency_overrides[get_current_user] = lambda: test_user

        other_field = Field(name="Другое поле")
        db_session.add(other_field)
        await db_session.commit()
        await db_session.refresh(other_field)
        room_other = Room(
            room_number="999",
            field_id=other_field.id,
            capacity=2,
            status=0,
        )
        db_session.add(room_other)
        await db_session.commit()
        await db_session.refresh(room_other)

        payload = {
            "customer": test_customer.name,
            "contract_date": date.today().isoformat(),
            "eol_fio": "Иванов",
            "position": "Инж",
            "field_id": test_field.id,
            "check_in": date.today().isoformat(),
            "check_out": (date.today() + timedelta(days=1)).isoformat(),
            "room_id": room_other.id,
            "comment": "",
        }
        response = await client.post("/api/requests/", json=payload)
        assert response.status_code == 400

    async def test_available_invalid_dates(self, client, test_field):
        response = await client.get(f"/api/requests/available?field_id={test_field.id}&check_in=2024-01-05&check_out=2024-01-01")
        assert response.status_code == 400

    async def test_available_field_not_found(self, client):
        response = await client.get("/api/requests/available?field_id=999&check_in=2024-01-01&check_out=2024-01-05")
        assert response.status_code == 400

    async def test_patch_approved_request(self, client, db_session, admin_user, test_field, test_customer, test_room):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=test_room.id,
            status="approved",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        payload = {"comment": "новый комментарий"}
        response = await client.patch(f"/api/requests/{req.id}", json=payload)
        assert response.status_code == 409

    @pytest.mark.xfail(reason="known bug: PATCH allows setting status to approved")
    async def test_patch_try_set_status_approved(self, client, db_session, admin_user, test_field, test_customer, test_room):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user
        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=test_room.id,
            status="pending",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        payload = {"status": "approved"}
        response = await client.patch(f"/api/requests/{req.id}", json=payload)
        # При исправлении бага должен вернуть 409
        assert response.status_code == 409

        @pytest.mark.xfail(reason="known bug: PATCH allows setting status to approved")
        async def test_patch_try_set_status_approved_xfail(self, client, db_session, admin_user, test_field, test_customer, test_room):
            client.app.dependency_overrides[get_current_user] = lambda: admin_user

            req = Request_before(
                customer=test_customer.name,
                contract_num="Д-1",
                contract_date=date.today(),
                eol_fio="Иванов",
                user_id=admin_user.id,
                position="Инж",
                field_id=test_field.id,
                check_in=date.today(),
                check_out=date.today() + timedelta(days=1),
                days=1,
                room_id=test_room.id,
                status="pending",
            )
            db_session.add(req)
            await db_session.commit()
            await db_session.refresh(req)

            payload = {"status": "approved"}
            response = await client.patch(f"/api/requests/{req.id}", json=payload)
            assert response.status_code == 409

    async def test_pending_field_admin_sees_only_own(self, client, db_session, test_field, field_admin_user):
        client.app.dependency_overrides[get_current_user] = lambda: field_admin_user

        req_own = Request_before(
            customer="ООО",
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=field_admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="pending",
        )
        db_session.add(req_own)
        other_field = Field(name="Другое")
        db_session.add(other_field)
        await db_session.commit()
        req_other = Request_before(
            customer="ООО",
            contract_num="Д-2",
            contract_date=date.today(),
            eol_fio="Петров",
            user_id=field_admin_user.id,
            position="Инж",
            field_id=other_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="pending",
        )
        db_session.add(req_other)
        await db_session.commit()

        response = await client.get("/api/requests/pending")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["field_id"] == test_field.id

    async def test_pending_admin_sees_all(self, client, db_session, admin_user):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        for i in range(3):
            req = Request_before(
                customer=f"ООО{i}",
                contract_num=f"Д-{i}",
                contract_date=date.today(),
                eol_fio=f"ФИО{i}",
                user_id=admin_user.id,
                position="Инж",
                field_id=1,
                check_in=date.today(),
                check_out=date.today() + timedelta(days=1),
                days=1,
                room_id=None,
                status="pending",
            )
            db_session.add(req)
        await db_session.commit()

        response = await client.get("/api/requests/pending")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    async def test_delete_other_user_request(self, client, db_session, test_user, test_role_user, test_field, test_customer):
        other_user = User(username="other", password="hashed", role_id=test_role_user.id)
        db_session.add(other_user)
        await db_session.commit()
        await db_session.refresh(other_user)

        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=other_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="pending",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        client.app.dependency_overrides[get_current_user] = lambda: test_user
        response = await client.delete(f"/api/requests/{req.id}")
        assert response.status_code == 403

    async def test_delete_approved_request(self, client, db_session, admin_user, test_field, test_customer):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="approved",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        response = await client.delete(f"/api/requests/{req.id}")
        assert response.status_code == 409

    async def test_approve_already_approved(self, client, db_session, admin_user, test_field, test_customer):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="approved",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        response = await client.post(f"/api/requests/{req.id}/approve")
        assert response.status_code == 409

    async def test_approve_rejected(self, client, db_session, admin_user, test_field, test_customer):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="rejected",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        response = await client.post(f"/api/requests/{req.id}/approve")
        assert response.status_code == 409

    async def test_reject_already_rejected(self, client, db_session, admin_user, test_field, test_customer):
        client.app.dependency_overrides[get_current_user] = lambda: admin_user

        req = Request_before(
            customer=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=admin_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            room_id=None,
            status="rejected",
        )
        db_session.add(req)
        await db_session.commit()
        await db_session.refresh(req)

        response = await client.post(f"/api/requests/{req.id}/reject")
        assert response.status_code == 409