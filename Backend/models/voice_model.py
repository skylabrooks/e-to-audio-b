from pymongo.collection import Collection


class Voice:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_all(self, page: int = 1, page_size: int = 100):
        return (
            self.collection.find({}, {"_id": 0})
            .skip((page - 1) * page_size)
            .limit(page_size)
        )

    def get_by_language(self, language_code: str, page: int = 1, page_size: int = 100):
        return (
            self.collection.find(
                {"language_codes": {"$regex": f"^{language_code}", "$options": "i"}},
                {"_id": 0},
            )
            .skip((page - 1) * page_size)
            .limit(page_size)
        )

    def get_filtered(self, filters: dict, page: int = 1, per_page: int = 100):
        """
        Retrieves voices from the database based on a set of filters,
        with pagination.

        Args:
            filters (dict): A dictionary of filters to apply to the query.
                            e.g., {"language_codes": "en", "ssml_gender": "FEMALE"}
            page (int): The page number to retrieve.
            per_page (int): The number of results per page.

        Returns:
            A cursor to the list of voices.
        """
        query = filters or {}
        return (
            self.collection.find(query, {"_id": 0})
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
