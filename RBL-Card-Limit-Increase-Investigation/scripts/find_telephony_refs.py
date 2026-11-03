from androguard.core.dex import DEX

path = "recovery/payload_analysis/inner_apk/classes.dex"

with open(path, "rb") as f:
    dex = DEX(f.read())

needles = (
    "SmsManager",
    "sendTextMessage",
    "sendMultipartTextMessage",
    "sendDataMessage",
    "sendUssdRequest",
)

for cls in dex.get_classes():
    for method in cls.get_methods():
        code = method.get_code()
        if code is None:
            continue

        for ins in code.get_bc().get_instructions():
            output = ins.get_output()
            if any(n.lower() in output.lower() for n in needles):
                print(
                    f"\nCLASS: {cls.get_name()}"
                    f"\nMETHOD: {method.get_name()}"
                    f"\nINSTRUCTION: {ins.get_name()} {output}"
                )