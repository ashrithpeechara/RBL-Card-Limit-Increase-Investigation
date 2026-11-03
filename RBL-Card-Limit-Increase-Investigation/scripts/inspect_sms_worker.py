from androguard.core.dex import DEX

path = "recovery/payload_analysis/inner_apk/classes.dex"
targets = {"Li2/s;", "Ly0/e;", "Ly0/l;"}

with open(path, "rb") as f:
    dex = DEX(f.read())

for cls in dex.get_classes():
    if cls.get_name() not in targets:
        continue

    print("\n" + "=" * 80)
    print("CLASS:", cls.get_name())

    for method in cls.get_methods():
        print("\nMETHOD:", method.get_name(), method.get_descriptor())

        code = method.get_code()
        if code is None:
            print("  [No code]")
            continue

        try:
            for ins in code.get_bc().get_instructions():
                print(f"  {ins.get_name():28} {ins.get_output()}")
        except Exception as exc:
            print("  [Instruction decoding failed]", repr(exc))