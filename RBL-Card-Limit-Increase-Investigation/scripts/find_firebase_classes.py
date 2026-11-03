from androguard.misc import AnalyzeAPK

apk_path = "recovery/payload_analysis/payload.decrypted"
a, dex_list, analysis = AnalyzeAPK(apk_path)

needles = (
    "FirebaseDatabase",
    "FirebaseApp",
    "FirebaseOptions",
    "getReference",
    "setDatabaseUrl",
    "setProjectId",
    "firebase_database_url",
    "default-rtdb.firebaseio.com",
)

for dex in dex_list:
    for cls in dex.get_classes():
        class_name = cls.get_name()
        hits = []

        for method in cls.get_methods():
            code = method.get_code()
            if not code:
                continue

            for ins in code.get_bc().get_instructions():
                output = ins.get_output()
                if any(n.lower() in output.lower() for n in needles):
                    hits.append(
                        f"  METHOD {method.get_name()}{method.get_descriptor()}\n"
                        f"    {ins.get_name()} {output}"
                    )

        if hits:
            print(f"\nCLASS {class_name}")
            print("\n".join(hits))