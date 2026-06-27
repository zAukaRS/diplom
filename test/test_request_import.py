import pytest
from datetime import date, timedelta
from sqlalchemy import select

from app.request_import import (
    import_requests_from_excel,
    _import_row,
    deduplicate_rows,
)
from app.models import Request, Request_before, Field, Customer, Resident, Room
from app.excel_parser import ParsedRequestRow
from conftest import create_excel_file


@pytest.mark.asyncio
class TestImportRow:

    async def test_missing_required_fields(self, db_session, test_user):
        stats = MockStats()
        row = ParsedRequestRow(
            full_name="",
            position=None,
            field_name="",
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            customer_name=None,
            contract_num=None,
            contract_date=None,
            eol_fio=None,
            is_full_form=True,
            sheet_name="Sheet1",
            row_number=1,
        )
        # Добавляем resident_cache={}
        await _import_row(db_session, row, test_user.id, stats, verbose=False, allow_missing_contract=False, resident_cache={})
        assert stats.rows_skipped == 1
        assert len(stats.errors) == 1

    async def test_field_not_found(self, db_session, test_user):
        stats = MockStats()
        row = ParsedRequestRow(
            full_name="Иван",
            position="Инж",
            field_name="Несуществующее",
            check_in=date.today(),
            check_out=date.today() + timedelta(days=1),
            days=1,
            customer_name="ООО",
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            is_full_form=True,
            sheet_name="Sheet1",
            row_number=1,
        )
        with pytest.raises(Exception):
            await _import_row(db_session, row, test_user.id, stats, verbose=False, allow_missing_contract=False, resident_cache={})

    @pytest.mark.xfail(reason="known bug: duplicate detection not implemented in _import_row")
    async def test_exact_duplicate(self, db_session, test_user, test_field, test_room, test_customer):
        existing_req = Request(
            customer_id=test_customer.id,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=test_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date(2024, 1, 1),
            check_out=date(2024, 1, 5),
            days=4,
            room_id=test_room.id,
            status="approved",
        )
        db_session.add(existing_req)
        await db_session.commit()

        stats = MockStats()
        row = ParsedRequestRow(
            full_name="Иван",
            position="Инж",
            field_name=test_field.name,
            check_in=date(2024, 1, 1),
            check_out=date(2024, 1, 5),
            days=4,
            customer_name=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            is_full_form=True,
            sheet_name="Sheet1",
            row_number=1,
        )
        await _import_row(db_session, row, test_user.id, stats, verbose=False, allow_missing_contract=False, resident_cache={})
        assert stats.duplicates_skipped == 1

    @pytest.mark.xfail(reason="known bug: replace existing request not implemented")
    async def test_replace_existing(self, db_session, test_user, test_field, test_room, test_customer):
        existing_req = Request(
            customer_id=test_customer.id,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            user_id=test_user.id,
            position="Инж",
            field_id=test_field.id,
            check_in=date(2024, 1, 1),
            check_out=date(2024, 1, 5),
            days=4,
            room_id=test_room.id,
            status="approved",
        )
        db_session.add(existing_req)
        await db_session.commit()
        old_id = existing_req.id

        stats = MockStats()
        row = ParsedRequestRow(
            full_name="Иван",
            position="Инж",
            field_name=test_field.name,
            check_in=date(2024, 2, 1),
            check_out=date(2024, 2, 5),
            days=4,
            customer_name=test_customer.name,
            contract_num="Д-2",
            contract_date=date.today(),
            eol_fio="Иванов",
            is_full_form=True,
            sheet_name="Sheet1",
            row_number=1,
        )
        await _import_row(db_session, row, test_user.id, stats, verbose=False, allow_missing_contract=False, resident_cache={})
        reqs = await db_session.execute(select(Request))
        all_reqs = reqs.scalars().all()
        assert len(all_reqs) == 1
        assert all_reqs[0].id != old_id
        assert all_reqs[0].check_in == date(2024, 2, 1)

    @pytest.mark.xfail(reason="known bug: room capacity not enforced correctly")
    async def test_room_capacity_1_two_rows(self, db_session, test_user, test_field, test_location, test_path, test_customer):
        room = Room(
            room_number="102",
            field_id=test_field.id,
            capacity=1,
            location_id=test_location.id,
            path_id=test_path.id,
            room_unique_id="102a",
            status=0,
        )
        db_session.add(room)
        await db_session.commit()
        await db_session.refresh(room)

        stats = MockStats()
        row1 = ParsedRequestRow(
            full_name="Иван",
            position="Инж",
            field_name=test_field.name,
            check_in=date(2024, 1, 1),
            check_out=date(2024, 1, 5),
            days=4,
            customer_name=test_customer.name,
            contract_num="Д-1",
            contract_date=date.today(),
            eol_fio="Иванов",
            is_full_form=True,
            sheet_name="Sheet1",
            row_number=1,
        )
        row2 = ParsedRequestRow(
            full_name="Петр",
            position="Инж",
            field_name=test_field.name,
            check_in=date(2024, 1, 1),
            check_out=date(2024, 1, 5),
            days=4,
            customer_name=test_customer.name,
            contract_num="Д-2",
            contract_date=date.today(),
            eol_fio="Петров",
            is_full_form=True,
            sheet_name="Sheet1",
            row_number=2,
        )

        await _import_row(db_session, row1, test_user.id, stats, verbose=False, allow_missing_contract=False, resident_cache={})
        await _import_row(db_session, row2, test_user.id, stats, verbose=False, allow_missing_contract=False, resident_cache={})

        assert stats.approved_formal == 1
        assert stats.rejected_no_room == 1

    async def test_duplicate_file_twice(self, db_session, test_user, test_field, test_room, test_customer):
        # Используем будущие даты, чтобы не было expired
        future_check_in = date.today() + timedelta(days=10)
        future_check_out = future_check_in + timedelta(days=4)
        rows = [
            ["OOO", "D-1", "Ivanov", "Ivan", "Eng", test_field.name, future_check_in, future_check_out, 4]
        ]
        buf = create_excel_file(rows)
        stats1 = await import_requests_from_excel(db_session, buf, test_user.id, verbose=False, allow_missing_contract=True)
        assert stats1.approved_formal == 1
        buf.seek(0)
        stats2 = await import_requests_from_excel(db_session, buf, test_user.id, verbose=False, allow_missing_contract=True)
        assert stats2.duplicates_skipped == 1
        assert stats2.approved_formal == 0

    @pytest.mark.xfail(reason="known bug: rows_skipped not incremented for inverted dates")
    async def test_invalid_dates(self, db_session, test_user, test_field):
        # Даты инвертированы
        rows = [
            ["ООО", "Д-1", "Иванов", "Иван", "Инж", test_field.name, date(2024,1,5), date(2024,1,1), 4]
        ]
        buf = create_excel_file(rows)
        stats = await import_requests_from_excel(db_session, buf, test_user.id, verbose=False, allow_missing_contract=True)
        assert stats.rows_skipped == 1
        assert "дата заезда позже даты выезда" in stats.errors[0]

    async def test_allow_missing_contract_false(self, db_session, test_user, test_field):
        future_check_in = date.today() + timedelta(days=10)
        future_check_out = future_check_in + timedelta(days=4)
        rows = [
            ["ООО", "", "Иванов", "Иван", "Инж", test_field.name, future_check_in, future_check_out, 4]
        ]
        buf = create_excel_file(rows)
        stats = await import_requests_from_excel(db_session, buf, test_user.id, verbose=False, allow_missing_contract=False)
        assert stats.rows_skipped == 1
        assert "отсутствует номер договора" in stats.errors[0]

    async def test_allow_missing_contract_true(self, db_session, test_user, test_field, test_room):
        future_check_in = date.today() + timedelta(days=10)
        future_check_out = future_check_in + timedelta(days=4)
        rows = [
            ["ООО", "", "Иванов", "Иван", "Инж", test_field.name, future_check_in, future_check_out, 4]
        ]
        buf = create_excel_file(rows)
        stats = await import_requests_from_excel(db_session, buf, test_user.id, verbose=False, allow_missing_contract=True)
        assert stats.approved_formal == 1
        req = (await db_session.execute(select(Request))).scalars().first()
        assert req.contract_num is not None

    async def test_deduplicate_rows(self):
        rows = [
            ParsedRequestRow(
                full_name="Иван", position="", field_name="Поле",
                check_in=date(2024,1,1), check_out=date(2024,1,5), days=4,
                customer_name="ООО", contract_num="Д-1", contract_date=None,
                eol_fio="", is_full_form=True, sheet_name="Лист1", row_number=1
            ),
            ParsedRequestRow(
                full_name="Иван", position="", field_name="Поле",
                check_in=date(2024,1,1), check_out=date(2024,1,5), days=4,
                customer_name="ООО", contract_num="Д-2", contract_date=None,
                eol_fio="", is_full_form=True, sheet_name="Лист2", row_number=2
            ),
        ]
        deduped = deduplicate_rows(rows)
        assert len(deduped) == 1
        assert deduped[0].contract_num == "Д-2"


class MockStats:
    def __init__(self):
        self.approved_formal = 0
        self.approved_guest = 0
        self.rejected_no_room = 0
        self.duplicates_skipped = 0
        self.rows_skipped = 0
        self.errors = []
        self.customers_created = []
        self.fields_created = []
        self.residents_created = []
        self.days_mismatch_warnings = []
        self.resident_overlap_warnings = []