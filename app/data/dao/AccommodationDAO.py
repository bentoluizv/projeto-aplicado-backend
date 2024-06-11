from sqlite3 import Connection
from typing import List


class AccommodationDAO:
    def __init__(self, db: Connection):
        self.db = db

    def count(self):
        cursor = self.db.cursor()
        count = (
            cursor.execute("SELECT COUNT(*) FROM accommodation")
            .fetchone()
            .get("COUNT(*)")
        )
        return count

    def insert(self, accommodation) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO accommodation (created_at, name, status, total_guests, single_beds, double_beds, min_nights, price) VALUES (:created_at, :name, :status, :total_guests, :single_beds, :double_beds, :min_nights, :price);",
            accommodation,
        )

        id = cursor.lastrowid

        for amenitie in accommodation["amenities"]:
            cursor.execute("SELECT id FROM amenities WHERE amenitie = ?", (amenitie,))
            amenitie_id = cursor.fetchone()["id"]
            cursor.execute(
                "INSERT INTO amenities_per_accommodation (accommodation_id, amenitie_id) VALUES (?, ?)",
                (id, amenitie_id),
            )

        self.db.commit()

    def findBy(self, property: str, value: str):
        statement = f"SELECT a.id, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.id = apa.accommodation_id LEFT JOIN amenities AS am ON apa.amenitie_id = am.id WHERE a.{property} = ? GROUP BY a.id;"
        cursor = self.db.cursor()
        cursor.execute(statement, (value,))
        result = cursor.fetchone()

        if not result:
            return None

        if result["amenities"] is not None:
            amenities = result["amenities"]
            result["amenities"] = amenities.split(",")
        else:
            result["amenities"] = []

        return result

    def find_many(self) -> List:
        statement = "SELECT a.id, a.created_at, a.name, a.status, a.total_guests, a.single_beds, a.double_beds, a.min_nights, a.price, GROUP_CONCAT(am.amenitie) AS amenities FROM accommodation AS a LEFT JOIN amenities_per_accommodation AS apa ON a.id = apa.accommodation_id LEFT JOIN amenities AS am ON apa.amenitie_id = am.id GROUP BY a.id;"
        cursor = self.db.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()

        if len(rows) == 0:
            return []

        for row in rows:
            if row["amenities"] is not None:
                amenities = row["amenities"]
                row["amenities"] = amenities.split(",")
            else:
                row["amenities"] = []

        return rows

    def update(self, id: str, accommodation) -> None:
        statement = "UPDATE accommodation SET name = ?, status = ?, total_guests = ?, single_beds = ?, double_beds = ?, min_nights = ?, price = ? WHERE id = ?;"
        cursor = self.db.cursor()

        cursor.execute(
            statement,
            (
                accommodation["name"],
                accommodation["status"],
                accommodation["total_guests"],
                accommodation["single_beds"],
                accommodation["double_beds"],
                accommodation["min_nights"],
                accommodation["price"],
                id,
            ),
        )

        cursor.execute(
            "DELETE FROM amenities_per_accommodation WHERE accommodation_id = ?",
            (id,),
        )

        for amenitie in accommodation["amenities"]:
            cursor.execute("SELECT id FROM amenities WHERE amenitie = ?", (amenitie,))
            amenitie_id = cursor.fetchone()["id"]
            cursor.execute(
                "INSERT INTO amenities_per_accommodation (accommodation_id, amenitie_id) VALUES (?, ?)",
                (id, str(amenitie_id)),
            )

        self.db.commit()

    def delete(self, id: str):
        statement = "DELETE FROM accommodation WHERE id = ?"
        cursor = self.db.cursor()
        cursor.execute(statement, (id,))
        self.db.commit()
