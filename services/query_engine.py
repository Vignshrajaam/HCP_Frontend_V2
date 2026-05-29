class NamespaceQueryEngine:

    # -------------------------------
    # User-friendly aliases
    # -------------------------------
    FIELD_MAP = {

        "replication": "replicationEnabled",
        "versioning": "versioningEnabled",

        "s3": "isS3Enabled",
        "https": "isHttpsEnabled",

        "cloudOptimized": "cloudOptimized",

        "dpl": "dpl",

        "retention": "retentionType",
        "retentionDefault": "retentionDefault",

        "s3ObjectLock": "s3ObjectLock",

        "multipart": "multipart"
    }

    def __init__(self, namespaces):

        self.namespaces = namespaces

    # -------------------------------
    # Main search
    # -------------------------------
    def search(self, query):

        conditions = self.parse_query(query)

        results = []

        for ns in self.namespaces:

            raw = ns.get("raw", {})

            matched = True

            for field, operator, expected in conditions:

                # Resolve alias
                raw_field = self.FIELD_MAP.get(field, field)

                # Special derived field
                if field == "multipart":

                    actual = (
                        raw.get("isS3Enabled") is True and
                        raw.get("cloudOptimized") is True and
                        raw.get("aclsHonored") is True
                    )

                else:
                    actual = raw.get(raw_field)

                actual = str(actual).lower()
                expected = expected.lower()

                # -------------------------------
                # Equals
                # -------------------------------
                if operator == "=":

                    if actual != expected:
                        matched = False
                        break

                # -------------------------------
                # Not Equals
                # -------------------------------
                elif operator == "!=":

                    if actual == expected:
                        matched = False
                        break

            if matched:
                results.append(ns)

        return results

    # -------------------------------
    # Parse query
    # -------------------------------
    def parse_query(self, query):

        conditions = []

        # normalize AND
        query = query.replace("AND", "and")

        parts = query.split("and")

        for part in parts:

            part = part.strip()

            operator = None

            # -------------------------------
            # !=
            # -------------------------------
            if "!=" in part:

                field, value = part.split("!=", 1)
                operator = "!="

            # -------------------------------
            # =
            # -------------------------------
            elif "=" in part:

                field, value = part.split("=", 1)
                operator = "="

            else:
                continue

            conditions.append((
                field.strip(),
                operator,
                value.strip()
            ))

        return conditions
