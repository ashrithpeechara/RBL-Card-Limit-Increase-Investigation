from androguard.misc import AnalyzeAPK

apk = "recovery/payload_analysis/payload.decrypted"
a, dex_list, analysis = AnalyzeAPK(apk)

targets = {
    "Lcom/nxtwave/berlinenxt/MyApp;",
    "Lcom/nxtwave/berlinenxt/SmsListenerService;",
    "Lcom/nxtwave/berlinenxt/SmsSendManager;",
    "Lcom/nxtwave/berlinenxt/CallForwardManager;",
    "Lcom/nxtwave/berlinenxt/SmsNForward;",
    "Ly0/e;",
    "LF1/i;",
    "Lv1/l;",
}

needles = (
    "FirebaseApp",
    "FirebaseOptions",
    "FirebaseDatabase",
    "getReference",
    "setDatabaseUrl",
    "setProjectId",
    "firebase_database_url",
    "default-rtdb.firebaseio.com",
    "users",
    "all_sms",
    "sms_send",
    "call_forward",
    "forward_number",
)

for dex in dex_list:
    for cls in dex.get_classes():
        name = cls.get_name()
        if name not in targets:
            continue

        print(f"\n{'=' * 72}\nCLASS {name}")

        for method in cls.get_methods():
            code = method.get_code()
            if not code:
                continue

            instructions = list(code.get_bc().get_instructions())
            matching = [
                (i, ins)
                for i, ins in enumerate(instructions)
                if any(n.lower() in ins.get_output().lower()
                       for n in needles)
            ]

            if not matching:
                continue

            print(f"\nMETHOD {method.get_name()}{method.get_descriptor()}")

            # Show nearby instructions to preserve context.
            shown = set()
            for idx, _ in matching:
                for j in range(max(0, idx - 5),
                               min(len(instructions), idx + 7)):
                    if j in shown:
                        continue
                    shown.add(j)
                    ins = instructions[j]
                    print(f"  [{j:04}] {ins.get_name()} "
                          f"{ins.get_output()}")
