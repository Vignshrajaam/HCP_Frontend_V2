from services.query_engine import NamespaceQueryEngine


class InteractiveQueryService:

    def __init__(self, namespaces):

        self.query_engine = NamespaceQueryEngine(
            namespaces
        )

    # -------------------------------
    # Start interactive shell
    # -------------------------------
    def start(self):

        print(
            "\n🔎 Interactive "
            "Namespace Query Mode"
        )

        print(
            "Type 'exit' or "
            "'quit' to stop"
        )

        print(
            "\nAvailable namespace "
            "fields:\n"
        )

        fields = [

            "aclsEnabled",
            "aclsHonored",
            "allowErasureCoding",
            "allowPermissionAndOwnershipChanges",
            "appendEnabled",

            "atimeSynchronizationEnabled",
            "cachedIngestKEK",
            "cloudOptimized",
            "creationTimeMillis",
            "customMetadataFullTextIndexingEnabled",

            "customMetadataIndexingEnabled",
            "customMetadataIndexingExcludeList",
            "customMetadataParsingEnabled",
            "deleteMarkerEnabled",
            "description",

            "dpl",
            "dynamicDpl",
            "enterpriseMode",
            "hardQuota",
            "hashScheme",

            "httpSSOEnabled",
            "indexingDefault",
            "indexingEnabled",
            "isAuthoritative",
            "isCifsEnabled",

            "isHidden",
            "isHttpEnabled",
            "isHttpsEnabled",
            "isNfsEnabled",
            "isS3Enabled",

            "isSmtpEnabled",
            "isWebdavEnabled",
            "lowerName",
            "minimumRetentionAfterInitialUnspecified",
            "name",

            "namespace.tenant",
            "owner",
            "parentUUID",
            "permissionMask",
            "permissionMaskString",

            "readFromReplica",
            "replicationCollisionAction",
            "replicationCollisionDispositionDays",
            "replicationCollisionDispositionEnabled",
            "replicationEnabled",

            "retentionDefault",
            "retentionDispositionEnabled",
            "retentionType",
            "s3ObjectLock",
            "s3ObjectLockDefaultMillis",

            "searchEnabled",
            "servicePlan",
            "servicePlanEffective",
            "serviceRemoteSystemRequests",
            "shreddingDefault",

            "softQuota",
            "state",
            "tags",
            "unbalancedMode",
            "unversionedOverwriteEnabled",

            "uuid",
            "version",
            "versioningEnabled",
            "versioningKeepMillis",
            "versioningPruningEnabled",

            "wasVersioningEverEnabled"
        ]

        # ---------------------------------
        # Print in 5 columns
        # ---------------------------------
        for i in range(
            0,
            len(fields),
            4
        ):

            print(

                f"{fields[i]:<40}"

                f"{fields[i+1] if i+1 < len(fields) else '':<40}"

                f"{fields[i+2] if i+2 < len(fields) else '':<40}"

                f"{fields[i+3] if i+3 < len(fields) else '':<40}"

                
            )

        print("\nExample queries:")

        print(
            "  replicationEnabled=false"
        )

        print(
            "  dpl=1 and replicationEnabled=false"
        )

        print(
            "  isS3Enabled=true"
        )

        print(
            "  isS3Enabled=true and "
            "s3ObjectLock!=NONE"
        )

        print(
            "  cloudOptimized=false"
        )

        # ---------------------------------
        # Query Loop
        # ---------------------------------
        while True:

            query = input(
                "\nHCP Query > "
            ).strip()

            # Exit
            if query.lower() in [
                "exit",
                "quit"
            ]:

                print(
                    "\n👋 Exiting query mode"
                )

                break

            # Empty input
            if not query:

                continue

            # Run query
            results = (
                self.query_engine.search(
                    query
                )
            )

            print(

                f"\n🔍 Query Results "
                f"({len(results)} matches)\n"

            )

            if not results:

                print(
                    "No matching "
                    "namespaces found"
                )

                continue

            for ns in results:

                print(
                    f" - {ns['tenant']} / "
                    f"{ns['name']}"
                )
