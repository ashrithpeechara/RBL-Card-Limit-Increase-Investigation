from androguard.core.dex import DEX

dex_path = "recovery/payload_analysis/inner_apk/classes.dex"
needle = "https://z.devalphas.online/sb/rb3/fx/"

with open(dex_path, "rb") as f:
    dex = DEX(f.read())

found = False

for cls in dex.get_classes():
    if "Lcom/nxtwave/berlinenxt/MainActivity;" not in cls.get_name():
        continue

    print("CLASS:", cls.get_name())

    for method in cls.get_methods():
        if method.get_name() != "onCreate":
            continue

        code = method.get_code()
        if code is None:
            print("No DEX code available for onCreate")
            continue

        instructions = list(code.get_bc().get_instructions())

        for i, ins in enumerate(instructions):
            text = str(ins.get_output())
            if needle in text:
                found = True
                print("\nMETHOD:", method.get_name(), method.get_descriptor())
                print("URL instruction index:", i)
                print("\n--- Nearby DEX instructions ---")

                start = max(0, i - 25)
                end = min(len(instructions), i + 50)

                for j in range(start, end):
                    marker = ">>" if j == i else "  "
                    print(f"{marker} [{j:04}] "
                          f"{instructions[j].get_name()} "
                          f"{instructions[j].get_output()}")

if not found:
    print("URL instruction not found in MainActivity.onCreate().")